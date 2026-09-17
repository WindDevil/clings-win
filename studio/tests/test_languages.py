"""The language layer: what the editor asks, and what it gets back.

The claims under test are the ones the design rests on:

* a language is picked by extension, and a file nobody claims is still
  editable (plain.py is a language, not a failure);
* the diagnostics come from the compiler the exercise is built with, so they
  cannot disagree with what `run` will say;
* the text being checked is the editor's buffer, not the file on disk, and
  checking writes nothing into exercises/; and
* every path that comes back is package-relative - a learner should never be
  shown the temporary directory their exercise was copied into.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from .. import paths
from ..languages import LANGUAGES, FALLBACK, all_languages, by_id, for_path
from ..languages.base import CheckContext, Language
from ..languages.c import CLanguage
from ..languages.plain import PLAIN
from . import harness
from .harness import IMPLICIT, NO_SEMICOLON, solution

# Both exercises below are used only through their reference answers, so the
# tests do not care what the learner has done to the files themselves.
SIMPLE = "00_basics/01_printf"
PROJECT = "17_translation_units/01_header_source_split"


class Registry(unittest.TestCase):
    """Which language opens which file."""

    def test_c_owns_c_and_h(self) -> None:
        self.assertIs(for_path("main.c"), LANGUAGES[0])
        self.assertIs(for_path("math_utils.h"), LANGUAGES[0])
        self.assertIs(for_path(Path("exercises/00_basics/01_printf.c")), LANGUAGES[0])

    def test_case_does_not_matter(self) -> None:
        self.assertIs(for_path("MAIN.C"), LANGUAGES[0])

    def test_an_unclaimed_file_is_still_editable(self) -> None:
        # Not None and not an error: a README opened by accident should be
        # readable in the editor, just with nothing clever to say about it.
        self.assertIs(for_path("notes.md"), FALLBACK)
        self.assertIs(for_path("Makefile"), FALLBACK)

    def test_the_longest_extension_wins(self) -> None:
        # Two extensions can only both match one name when one is a suffix of
        # the other, which is what compound extensions are for: archive.tar.gz
        # ends in both ".gz" and ".tar.gz".
        class Short(Language):
            id = "short"
            extensions = (".gz",)

        class Long(Language):
            id = "long"
            extensions = (".tar.gz",)

        import studio.languages as registry

        original = registry.LANGUAGES
        try:
            registry.LANGUAGES = (Short(), Long())
            self.assertIs(for_path("archive.tar.gz"), registry.LANGUAGES[1])
            self.assertIs(for_path("archive.gz"), registry.LANGUAGES[0])
        finally:
            registry.LANGUAGES = original

    def test_by_id(self) -> None:
        self.assertIs(by_id("c"), LANGUAGES[0])
        self.assertIs(by_id("plain"), PLAIN)
        self.assertIsNone(by_id("cobol"))

    def test_ids_and_extensions_do_not_collide(self) -> None:
        ids = [language.id for language in all_languages()]
        self.assertEqual(len(ids), len(set(ids)), f"语言 id 重了: {ids}")
        claimed: dict[str, str] = {}
        for language in LANGUAGES:
            for extension in language.extensions:
                self.assertNotIn(
                    extension, claimed, f"{extension} 被两个语言同时认领"
                )
                claimed[extension] = language.id

    def test_describe_tells_the_browser_what_to_offer(self) -> None:
        described = CLanguage().describe()
        self.assertEqual(described["id"], "c")
        self.assertTrue(described["checks"])
        self.assertTrue(described["completes"])
        self.assertEqual(described["editor_mode"], "text/x-csrc")
        # The fallback has to be honest about doing nothing: the page shows no
        # diagnostics button for it rather than a button that answers nothing.
        self.assertFalse(PLAIN.describe()["checks"])
        self.assertFalse(PLAIN.describe()["completes"])


class PlainLanguage(unittest.TestCase):
    def test_it_answers_nothing_and_does_not_pretend_otherwise(self) -> None:
        context = CheckContext(toolchain=None, root=harness.ROOT)  # type: ignore[arg-type]
        self.assertEqual(PLAIN.check(Path("a.md"), "x", context), [])
        self.assertEqual(PLAIN.completions(Path("a.md"), "x", context), [])


class CWithoutACompiler(unittest.TestCase):
    """No compiler is a thing to report, not a thing to crash on."""

    def test_check_says_so_instead_of_raising(self) -> None:
        import dataclasses

        toolchain = dataclasses.replace(harness.toolchain(), compiler_found=False)
        context = CheckContext(toolchain=toolchain, root=harness.ROOT)
        found = CLanguage().check(Path("main.c"), "int main(void){return 0;}", context)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].severity, "info")
        self.assertIn("doctor", found[0].message)


class CCapabilities(unittest.TestCase):
    def test_it_checks_and_completes(self) -> None:
        self.assertTrue(CLanguage().checks)
        self.assertTrue(CLanguage().completes)


@unittest.skipUnless(harness.compiler_ready(), "没有编译器，跳过 C 语法检查")
class CDiagnostics(unittest.TestCase):
    """What the compiler says, turned into something an editor can draw."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.language = CLanguage()
        cls.context = harness.check_context(SIMPLE)

    def check(self, content: str, ident: str = SIMPLE):
        target = harness.files_of(ident)[0]
        return self.language.check(target, content, harness.check_context(ident))

    def assert_package_relative(self, diagnostics) -> None:
        """No diagnostic may name a temporary directory or an absolute path."""
        for item in diagnostics:
            self.assertFalse(
                item.file.startswith("/") or ":" in item.file or item.file.startswith(".."),
                f"诊断里的路径不是包内相对路径: {item.file!r}",
            )

    def test_a_correct_answer_is_clean(self) -> None:
        found = self.check(solution(SIMPLE))
        self.assertEqual([item.message for item in found], [])

    def test_text_is_not_the_file_on_disk(self) -> None:
        # The buffer is what gets compiled.  The exercise on disk is the
        # unsolved template here, which compiles; only the text handed in has
        # the mistake, so a diagnostic proves the buffer was the input.
        target = harness.files_of(SIMPLE)[0]
        on_disk = target.read_text(encoding="utf-8")
        self.assertNotEqual(on_disk, solution(SIMPLE), "这个练习的模板变了")
        found = self.check(solution(SIMPLE) + NO_SEMICOLON)
        self.assertTrue(found, "故意写坏的代码没有报错")
        self.assertEqual(target.read_text(encoding="utf-8"), on_disk)

    def test_checking_writes_nothing_into_the_tree(self) -> None:
        target = harness.files_of(SIMPLE)[0]
        before = {path: path.read_bytes() for path in harness.files_of(SIMPLE)}
        self.check(solution(SIMPLE) + NO_SEMICOLON)
        after = {path: path.read_bytes() for path in harness.files_of(SIMPLE)}
        self.assertEqual(before, after, f"{target.name} 的目录被检查改动了")

    def test_its_temporary_directory_does_not_survive(self) -> None:
        pattern = "clings-check-*"
        parent = Path(tempfile.gettempdir())
        before = {item.name for item in parent.glob(pattern)}
        self.check(solution(SIMPLE) + NO_SEMICOLON)
        left = {item.name for item in parent.glob(pattern)} - before
        self.assertEqual(left, set(), f"检查留下了临时目录: {left}")

    def test_a_missing_semicolon_points_at_the_line_it_is_on(self) -> None:
        text = solution(SIMPLE) + NO_SEMICOLON
        found = self.check(text)
        self.assertTrue(found)
        first = found[0]
        self.assertEqual(first.severity, "error")
        self.assertEqual(first.file, paths.relative(harness.files_of(SIMPLE)[0]))
        # The appended function starts on the line after the trailing blank.
        self.assertEqual(first.line, len(solution(SIMPLE).splitlines()) + 2)
        self.assertIn(";", first.message)
        # The carets gcc echoes back are what make the message legible, so
        # they have to survive into the context the page shows.
        self.assertIn("clings_probe_unsolved", first.context)

    def test_an_unknown_function_is_an_error_under_werror(self) -> None:
        found = self.check(solution(SIMPLE) + IMPLICIT)
        self.assertTrue(found)
        messages = " ".join(item.message for item in found)
        self.assertIn("clings_probe_missing", messages)
        self.assertEqual(found[0].severity, "error")

    def test_a_warning_names_the_flag_that_made_it_fatal(self) -> None:
        # -Werror is in the runner's own cflags, so a format mismatch arrives
        # as an error; the flag is what tells the learner which rule it broke.
        # The mismatch is made in the reference answer's own call, because
        # that is the mistake a learner makes in this exercise.
        text = solution(SIMPLE)
        broken = text.replace(
            'printf("Hello, C!\\n")', 'printf("%d\\n", "oops")'
        )
        self.assertNotEqual(broken, text, "参考答案里的 printf 变了，这个测试要跟着改")
        found = self.check(broken)
        codes = [item.code for item in found]
        self.assertIn("-Werror=format=", codes)
        flagged = next(item for item in found if item.code == "-Werror=format=")
        self.assertIn("char *", flagged.message)
        self.assertEqual(flagged.severity, "error")

    def test_a_header_is_reported_as_the_header(self) -> None:
        # A header cannot be checked on its own - it does not compile by
        # itself - so the exercise is checked with the edited header in place,
        # and the answer has to name the header the learner was looking at.
        header = next(path for path in harness.files_of(PROJECT) if path.suffix == ".h")
        content = header.read_text(encoding="utf-8") + NO_SEMICOLON
        found = self.language.check(header, content, harness.check_context(PROJECT))
        self.assertTrue(found, "改坏的 .h 没有报错")
        self.assertEqual(found[0].file, paths.relative(header))
        # ...and it says how it got there: the same header is compiled once
        # per .c file that includes it, so the chain is the only thing that
        # could differ between those reports.
        self.assertIn("经由", found[0].context)

    def test_every_path_that_comes_back_is_package_relative(self) -> None:
        self.assert_package_relative(self.check(solution(SIMPLE) + NO_SEMICOLON))
        header = next(path for path in harness.files_of(PROJECT) if path.suffix == ".h")
        self.assert_package_relative(
            self.language.check(
                header,
                header.read_text(encoding="utf-8") + NO_SEMICOLON,
                harness.check_context(PROJECT),
            )
        )

    def test_the_edited_file_comes_first(self) -> None:
        # Break the header *and* the file being edited: the page is showing
        # the second one, so that is the problem it should lead with.
        main = harness.files_of(PROJECT)[0]
        header = next(path for path in harness.files_of(PROJECT) if path.suffix == ".h")
        original = main.read_text(encoding="utf-8")
        with harness.unchanged(header):
            header.write_text(
                header.read_text(encoding="utf-8") + NO_SEMICOLON, encoding="utf-8"
            )
            found = self.language.check(
                main, original + IMPLICIT, harness.check_context(PROJECT)
            )
        self.assertTrue(len(found) >= 2, f"两个错误只报了一个: {found}")
        self.assertEqual(found[0].file, paths.relative(main))

    def test_one_mistake_in_a_header_is_reported_once(self) -> None:
        # A header included by two .c files is compiled twice, and gcc says so
        # twice.  The list the learner reads should not.
        header = next(path for path in harness.files_of(PROJECT) if path.suffix == ".h")
        found = self.language.check(
            header,
            header.read_text(encoding="utf-8") + NO_SEMICOLON,
            harness.check_context(PROJECT),
        )
        keys = [(item.file, item.line, item.column, item.message) for item in found]
        self.assertEqual(len(keys), len(set(keys)), f"同一条诊断重复了: {keys}")


@unittest.skipUnless(harness.compiler_ready(), "没有编译器")
class CCompletions(unittest.TestCase):
    """What the learner could type next."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.language = CLanguage()

    def complete(self, text: str, ident: str = SIMPLE):
        target = harness.files_of(ident)[0]
        items = self.language.completions(target, text, harness.check_context(ident))
        return {item.label: item for item in items}

    def test_the_standard_library_comes_with_its_signature(self) -> None:
        items = self.complete(solution(SIMPLE))
        self.assertIn("printf", items)
        printf = items["printf"]
        self.assertEqual(printf.kind, "function")
        self.assertEqual(printf.header, "<stdio.h>")
        self.assertIn("printf(", printf.detail)

    def test_keywords_types_and_snippets(self) -> None:
        items = self.complete(solution(SIMPLE))
        self.assertEqual(items["for"].kind, "keyword")
        self.assertEqual(items["size_t"].kind, "type")

    def test_a_snippet_pastes_a_body_not_a_name(self) -> None:
        # Asked with an empty buffer on purpose: a file that already defines
        # main shadows the snippet with its own declaration, and then the
        # completion is the name - which is right, but is not this test.
        items = self.complete("")
        main = items["main"]
        self.assertEqual(main.kind, "snippet")
        self.assertIn("int main", main.insert)
        self.assertIn("return", main.insert)
        # The body is what gets pasted; the detail is the label a person
        # reads in the popup, and the label is the key it is filed under.
        self.assertEqual(main.label, "main")
        self.assertNotEqual(main.detail, main.label)

    def test_the_exercises_own_names_are_offered(self) -> None:
        # A symbol that only exists in this exercise's other file, which is
        # the part a table of the standard library could never know.
        items = self.complete("", PROJECT)
        locals_ = {label: item for label, item in items.items() if item.header == "本练习"}
        self.assertTrue(locals_, "练习自己声明的名字没有出现在补全里")

    def test_what_the_learner_wrote_wins_over_the_table(self) -> None:
        text = "int printf(void) { return 0; }\n"
        items = self.complete(text)
        self.assertEqual(items["printf"].header, "本练习")

    def test_the_bundled_test_framework_is_offered(self) -> None:
        items = self.complete(solution(SIMPLE))
        self.assertIn("CLINGS_CHECK", items)
        self.assertEqual(items["CLINGS_CHECK"].header, "clings/test.h")

    def test_the_list_is_sorted_and_unique(self) -> None:
        labels = [
            item.label
            for item in self.language.completions(
                harness.files_of(SIMPLE)[0],
                solution(SIMPLE),
                harness.check_context(SIMPLE),
            )
        ]
        self.assertEqual(labels, sorted(labels))
        self.assertEqual(len(labels), len(set(labels)))
        self.assertGreater(len(labels), 150)
