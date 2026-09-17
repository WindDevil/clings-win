"""The rest of the studio: the runner contract, the path rules, and the menu.

Three things that are easy to get wrong and cheap to pin down:

* ``bridge`` reads the runner's JSON.  Those field names are a contract with a
  generated file, held on the other end by ``tools/sync_from_source.py``, so
  the tests read the real thing rather than a fixture;
* ``paths`` decides what the editor may touch, and everything the server does
  goes through it; and
* the double-click path - no arguments, run the exercise, then stay open -
  which is the behaviour a learner meets first and the one hardest to check by
  hand, because it needs a file manager.
"""

from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from .. import bridge, menu, paths, vscode
from ..bridge import Exercise, Listing, RunResult, Topic
from . import harness

SIMPLE = "00_basics/01_printf"
PROJECT = "17_translation_units/01_header_source_split"


class Paths(unittest.TestCase):
    """What the editor is allowed to name."""

    def test_inside_the_package_is_allowed(self) -> None:
        target = paths.resolve_within(paths.ROOT, "exercises/00_basics/01_printf.c")
        self.assertTrue(target.is_file())

    def test_the_root_itself_is_inside_itself(self) -> None:
        self.assertEqual(paths.resolve_within(paths.ROOT, "."), paths.ROOT.resolve())

    def test_escapes_are_refused(self) -> None:
        for name in ("..", "../..", "exercises/../../etc/passwd", "../../clings"):
            with self.subTest(name=name):
                with self.assertRaises(paths.PathNotAllowed):
                    paths.resolve_within(paths.ROOT, name)

    def test_an_absolute_path_is_not_special_cased(self) -> None:
        # It resolves to itself, and then fails the containment check - there
        # is no branch here that trusts a caller for saying "/" out loud.
        with self.assertRaises(paths.PathNotAllowed):
            paths.resolve_within(paths.ROOT, "C:/Windows/win.ini" if
                                 paths.ROOT.drive else "/etc/passwd")

    def test_relative_is_the_json_spelling(self) -> None:
        target = paths.ROOT / "exercises" / "00_basics" / "01_printf.c"
        self.assertEqual(paths.relative(target), "exercises/00_basics/01_printf.c")
        self.assertNotIn("\\", paths.relative(target))

    def test_exercise_files_skips_what_it_cannot_resolve(self) -> None:
        bogus = Exercise(
            ident="x", topic="t", slug="s", title="", objective="", reference="",
            hint="", is_project=False, completed=False,
            files=("exercises/00_basics/01_printf.c", "../escape.c"), sources=(),
        )
        found = paths.exercise_files(bogus)
        self.assertEqual(len(found), 1)
        self.assertTrue(str(found[0]).endswith("01_printf.c"))

    def test_find_file_accepts_both_spellings(self) -> None:
        found = harness.exercise(SIMPLE)
        relative = paths.find_file(harness.listing(), found, found.main_file)
        absolute = paths.find_file(harness.listing(), found, str(relative))
        self.assertEqual(relative, absolute)

    def test_find_file_refuses_another_exercise(self) -> None:
        found = harness.exercise(SIMPLE)
        with self.assertRaises(paths.PathNotAllowed):
            paths.find_file(harness.listing(), found, f"exercises/{PROJECT}.c")

    def test_a_readme_is_not_editable_but_a_source_file_is(self) -> None:
        self.assertFalse(paths.is_editable(paths.ROOT / "exercises/00_basics/README.md"))
        self.assertTrue(paths.is_editable(harness.files_of(SIMPLE)[0]))


class TheRunnerContract(unittest.TestCase):
    """bridge.py against the real `clings list --json`."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.listing = harness.listing()

    def test_the_listing_is_complete(self) -> None:
        self.assertGreater(self.listing.total, 0)
        self.assertEqual(self.listing.total, len(self.listing.exercises))
        self.assertTrue(self.listing.topics)
        self.assertTrue(self.listing.launcher)
        self.assertEqual(
            self.listing.total,
            sum(len(topic.exercises) for topic in self.listing.topics),
        )

    def test_every_exercise_has_what_the_page_shows(self) -> None:
        for exercise in self.listing.exercises:
            with self.subTest(ident=exercise.ident):
                self.assertTrue(exercise.ident)
                self.assertTrue(exercise.title)
                self.assertTrue(exercise.objective)
                self.assertTrue(exercise.hint)
                self.assertTrue(exercise.files)
                # The file the editor opens first has to be a real one.
                self.assertTrue(exercise.slug)
                self.assertIn(exercise.ident, f"{exercise.topic}/{exercise.slug}")

    def test_progress_is_reported(self) -> None:
        self.assertIsInstance(self.listing.completed_count, int)
        self.assertLessEqual(self.listing.completed_count, self.listing.total)
        done = [item for item in self.listing.exercises if item.completed]
        self.assertEqual(len(done), self.listing.completed_count)

    def test_an_exact_name_resolves(self) -> None:
        found = self.listing.find(SIMPLE)
        self.assertIsNotNone(found)
        self.assertEqual(found.ident, SIMPLE)

    def test_a_slug_resolves_when_it_is_unambiguous(self) -> None:
        found = self.listing.find("05_getchar_putchar")
        self.assertIsNotNone(found)
        self.assertTrue(found.ident.endswith("/05_getchar_putchar"))

    def test_an_ambiguous_name_is_not_guessed(self) -> None:
        # `01_printf` is 00_basics/01_printf and 12_standard_library/01_printf_formats.
        # The runner refuses to guess and so does the studio; a wrong guess
        # would compile a different exercise than the learner asked for.
        self.assertIsNone(self.listing.find("01_printf"))
        candidates = self.listing.candidates("01_printf")
        self.assertGreater(len(candidates), 1)
        self.assertIn(SIMPLE, [item.ident for item in candidates])

    def test_an_unknown_name_has_no_candidates(self) -> None:
        self.assertIsNone(self.listing.find("no_such_exercise"))
        self.assertEqual(self.listing.candidates("no_such_exercise"), [])

    def test_the_next_exercise_is_the_first_unsolved_one(self) -> None:
        nxt = self.listing.next_exercise()
        if nxt is None:
            self.assertTrue(all(item.completed for item in self.listing.exercises))
        else:
            self.assertFalse(nxt.completed)
            order = [item.ident for item in self.listing.exercises]
            for earlier in order[: order.index(nxt.ident)]:
                self.assertTrue(self.listing.find(earlier).completed)

    def test_the_toolchain_is_readable(self) -> None:
        found = harness.toolchain()
        self.assertTrue(found.compiler)
        self.assertTrue(found.cflags, "运行器没有报告编译参数")
        self.assertIsInstance(found.compiler_found, bool)
        if found.compiler_found:
            self.assertTrue(found.compiler_version)

    def test_a_stage_has_a_label_the_page_can_show(self) -> None:
        for stage, expected in (
            ("compile", "编译失败"),
            ("timeout", "运行超时"),
        ):
            with self.subTest(stage=stage):
                self.assertEqual(
                    RunResult("x", "", False, stage, "").stage_label, expected
                )
        self.assertEqual(
            RunResult("x", "", True, "run", "").stage_label, "全部通过"
        )
        self.assertEqual(
            RunResult("x", "", False, "run", "").stage_label, "测试未通过"
        )

    def test_a_solution_is_source_text(self) -> None:
        text = harness.solution(SIMPLE)
        self.assertTrue(text.strip())
        self.assertIn("main", text)


class TheNextExercise(unittest.TestCase):
    """next_exercise() on a listing built by hand: no tree can be all-passed."""

    def build(self, *completed: bool) -> Listing:
        exercises = tuple(
            Exercise(
                ident=f"t/{index}", topic="t", slug=str(index), title="", objective="",
                reference="", hint="", is_project=False, completed=done, files=("f.c",),
                sources=(),
            )
            for index, done in enumerate(completed)
        )
        return Listing(
            root=str(paths.ROOT), launcher="clings.cmd", total=len(exercises),
            completed_count=sum(completed), topics=(Topic("t", exercises),),
        )

    def test_nothing_left(self) -> None:
        self.assertIsNone(self.build(True, True).next_exercise())

    def test_the_first_gap(self) -> None:
        self.assertEqual(self.build(True, False, False).next_exercise().ident, "t/1")

    def test_main_file_is_the_first_one(self) -> None:
        self.assertEqual(self.build(False).exercises[0].main_file, "f.c")


class TheMenu(unittest.TestCase):
    """The double-click flow: run, then stay open."""

    def build_listing(self, *completed: bool) -> Listing:
        """A listing whose progress the test decides, not the checkout.

        A developer's copy has real progress in .clings/, so a test about the
        first run cannot read it off the tree.
        """
        exercises = tuple(
            Exercise(
                ident=SIMPLE if index == 0 else f"t/{index}", topic="t", slug="s",
                title="标题", objective="目标", reference="", hint="提示",
                is_project=False, completed=done,
                files=("exercises/00_basics/01_printf.c",), sources=(),
            )
            for index, done in enumerate(completed)
        )
        return Listing(
            root=str(paths.ROOT), launcher="clings.cmd", total=len(exercises),
            completed_count=sum(completed), topics=(Topic("t", exercises),),
        )

    def run_menu(self, answers, ident: str = SIMPLE):
        """Run the menu with the terminal replaced and the runner intercepted.

        run_streaming() hands the real terminal to the exercise, which a test
        has no terminal for, and printing is what is under test - so both ends
        are captured and the runner is told nothing ran.
        """
        output = io.StringIO()
        calls: list[str] = []
        with mock.patch.object(
            menu.bridge, "run_streaming", side_effect=lambda name=None: calls.append(name) or 0
        ), mock.patch.object(menu, "choose", side_effect=list(answers)):
            with redirect_stdout(output):
                code = menu.run(ident)
        return code, output.getvalue(), calls

    def test_it_runs_and_stops(self) -> None:
        code, text, calls = self.run_menu(["0"])
        self.assertEqual(code, 0)
        self.assertEqual(calls, [SIMPLE])
        self.assertIn(SIMPLE, text)
        self.assertIn(harness.exercise(SIMPLE).title, text)

    def test_the_first_run_says_what_this_is(self) -> None:
        # The learner double-clicks a .cmd file having never used a terminal:
        # without this, the window is a compiler error and a menu.
        with mock.patch.object(menu.bridge, "listing", return_value=self.build_listing(False, False)):
            code, text, _ = self.run_menu(["0"])
        self.assertEqual(code, 0)
        self.assertIn("第一次用", text)
        self.assertIn("一开始不通过是正常的", text)
        self.assertIn("记事本", text)

    def test_every_run_names_the_file_to_edit(self) -> None:
        with mock.patch.object(menu.bridge, "listing", return_value=self.build_listing(False)):
            _, text, _ = self.run_menu(["0"])
        self.assertIn("要改的文件", text)
        self.assertIn("01_printf.c", text)

    def test_a_returning_learner_is_not_lectured_again(self) -> None:
        with mock.patch.object(menu.bridge, "listing", return_value=self.build_listing(True, False)):
            _, text, _ = self.run_menu(["0"])
        self.assertNotIn("第一次用", text)

    def test_it_repeats_on_demand(self) -> None:
        code, _, calls = self.run_menu(["1", "0"])
        self.assertEqual(code, 0)
        self.assertEqual(calls, [SIMPLE, SIMPLE])

    def test_it_shows_the_hint(self) -> None:
        code, text, _ = self.run_menu(["4", "0"])
        self.assertEqual(code, 0)
        self.assertIn(harness.exercise(SIMPLE).hint, text)

    def test_nonsense_asks_again(self) -> None:
        code, text, _ = self.run_menu(["7", "0"])
        self.assertEqual(code, 0)
        self.assertIn("请输入", text)

    def test_an_unknown_name_is_an_error(self) -> None:
        code, _, error = self.fail_to_start("no_such_exercise")
        self.assertEqual(code, 1)
        self.assertIn("找不到", error)

    def test_an_ambiguous_name_lists_the_candidates(self) -> None:
        code, _, error = self.fail_to_start("01_printf")
        self.assertEqual(code, 1)
        self.assertIn("歧义", error)
        self.assertIn(SIMPLE, error)

    def fail_to_start(self, ident: str):
        """A run that never starts: the report belongs on stderr.

        Nothing here is a result the learner asked to read - it is why the
        thing they asked for did not happen - so it goes to stderr and leaves
        stdout for the exercise.
        """
        error = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(error):
            code = menu.run(ident)
        return code, "", error.getvalue()

    def test_nothing_left_to_do_says_so(self) -> None:
        empty = Listing(
            root=str(paths.ROOT), launcher="clings.cmd", total=0, completed_count=0,
            topics=(),
        )
        with mock.patch.object(menu.bridge, "listing", return_value=empty):
            with redirect_stdout(io.StringIO()):
                code = menu.run(None)
        self.assertEqual(code, 1)

    def test_a_broken_runner_is_reported_not_raised(self) -> None:
        error = io.StringIO()
        with mock.patch.object(
            menu.bridge, "listing", side_effect=bridge.RunnerError("no runner")
        ):
            with redirect_stdout(io.StringIO()), redirect_stderr(error):
                code = menu.run(None)
        self.assertEqual(code, 1)
        self.assertIn("no runner", error.getvalue())


class ChoosingFromTheMenu(unittest.TestCase):
    def test_eof_means_stop(self) -> None:
        with mock.patch("builtins.input", side_effect=EOFError):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(menu.choose(harness.exercise(SIMPLE)), "0")

    def test_interrupt_means_stop(self) -> None:
        with mock.patch("builtins.input", side_effect=KeyboardInterrupt):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(menu.choose(harness.exercise(SIMPLE)), "0")

    def test_the_choices_are_listed(self) -> None:
        labels = menu.choices(harness.exercise(SIMPLE))
        with mock.patch("builtins.input", return_value="1"):
            with redirect_stdout(io.StringIO()) as output:
                self.assertEqual(menu.choose(harness.exercise(SIMPLE)), "1")
        for key, label in labels:
            self.assertIn(f"[{key}]", output.getvalue())
            self.assertIn(label, output.getvalue())

    def test_the_editors_are_offered_by_name(self) -> None:
        # "用 VS Code 打开" without an object is how this menu read when a
        # beginner had no idea yet what the object was.
        labels = dict(menu.choices(harness.exercise(SIMPLE)))
        self.assertIn("01_printf.c", labels["2"])
        self.assertIn("内置编辑器", labels["3"])
        self.assertEqual([key for key, _ in menu.choices(harness.exercise(SIMPLE))],
                         ["1", "2", "3", "4", "0"])

    def test_the_menu_without_an_exercise_is_still_listed(self) -> None:
        with mock.patch("builtins.input", return_value="0"):
            with redirect_stdout(io.StringIO()) as output:
                self.assertEqual(menu.choose(), "0")
        self.assertIn("[1]", output.getvalue())


class TheLauncher(unittest.TestCase):
    """`python -m studio`: what clings.cmd calls, and with what."""

    def main(self, *argv: str):
        from ..__main__ import main

        return main(list(argv))

    def test_no_arguments_is_the_menu(self) -> None:
        # The double-click case: no help text at somebody who did not ask a
        # question, no argparse error - the next exercise and a menu.
        with mock.patch.object(menu, "run", return_value=0) as run:
            self.assertEqual(self.main(), 0)
        run.assert_called_once_with(None)

    def test_open_goes_to_vscode(self) -> None:
        with mock.patch.object(vscode, "main", return_value=0) as opened:
            self.assertEqual(self.main("open", SIMPLE), 0)
        opened.assert_called_once_with([SIMPLE])

    def test_open_without_an_exercise(self) -> None:
        with mock.patch.object(vscode, "main", return_value=0) as opened:
            self.main("open")
        opened.assert_called_once_with([])

    def test_web_starts_the_server(self) -> None:
        from .. import server

        with mock.patch.object(server, "serve", return_value=0) as serve:
            self.assertEqual(self.main("web", "--port", "0", "--no-browser"), 0)
        serve.assert_called_once_with(0, open_browser=False)

    def test_web_defaults_to_opening_a_browser(self) -> None:
        from .. import server

        with mock.patch.object(server, "serve", return_value=0) as serve:
            self.main("web")
        self.assertEqual(serve.call_args[0][0], server.DEFAULT_PORT)
        self.assertTrue(serve.call_args[1]["open_browser"])

    def test_menu_takes_an_exercise(self) -> None:
        with mock.patch.object(menu, "run", return_value=0) as run:
            self.main("menu", SIMPLE)
        run.assert_called_once_with(SIMPLE)

    def test_help_is_not_an_error(self) -> None:
        with redirect_stdout(io.StringIO()) as output:
            self.assertEqual(self.main("--help"), 0)
        self.assertIn("studio", output.getvalue())

    def test_a_mistyped_command_is_an_error(self) -> None:
        with redirect_stdout(io.StringIO()):
            self.assertEqual(self.main("nope"), 2)


class FindingAnEditor(unittest.TestCase):
    """Opening a file in VS Code, without opening a window in a test."""

    def test_an_explicit_choice_wins(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fake = Path(folder) / "code.cmd"
            fake.write_text("@echo off\n", encoding="utf-8")
            with mock.patch.dict("os.environ", {"CLINGS_VSCODE": str(fake)}):
                self.assertEqual(vscode.find_editor(), fake)

    def test_a_setting_that_points_nowhere_is_ignored(self) -> None:
        with mock.patch.dict("os.environ", {"CLINGS_VSCODE": "C:/nope/code.cmd"}):
            self.assertNotEqual(vscode.find_editor(), Path("C:/nope/code.cmd"))

    def test_the_plan_is_one_window_and_the_folder(self) -> None:
        with mock.patch.object(vscode, "find_editor", return_value=Path("code.cmd")):
            arguments = vscode.plan([paths.ROOT, paths.ROOT / "a.c"])
        self.assertEqual(arguments[0], "code.cmd")
        self.assertIn("--reuse-window", arguments)
        self.assertEqual(arguments[-1], str(paths.ROOT / "a.c"))

    def test_a_line_number_uses_goto(self) -> None:
        target = paths.ROOT / "a.c"
        with mock.patch.object(vscode, "find_editor", return_value=Path("code.cmd")):
            arguments = vscode.plan([target], line=12)
        self.assertIn("--goto", arguments)
        self.assertIn(f"{target}:12", arguments)

    def test_a_line_number_keeps_the_folder(self) -> None:
        # Without the folder the window has no workspace, so the include/
        # configuration that makes include/clings/test.h resolve is not loaded.
        target = paths.ROOT / "a.c"
        with mock.patch.object(vscode, "find_editor", return_value=Path("code.cmd")):
            arguments = vscode.plan([paths.ROOT, target], line=12)
        self.assertEqual(arguments[0], "code.cmd")
        self.assertIn(str(paths.ROOT), arguments)
        self.assertEqual(arguments[-2:], ["--goto", f"{target}:12"])

    def test_no_editor_is_an_error_with_a_way_out(self) -> None:
        with mock.patch.object(vscode, "find_editor", return_value=None):
            with self.assertRaises(FileNotFoundError) as caught:
                vscode.plan([paths.ROOT])
        # The message has to lead somewhere: the bundled editor is the way out
        # for a learner who has no VS Code.
        self.assertIn("web", str(caught.exception))

    def test_no_targets_is_a_programming_error(self) -> None:
        with mock.patch.object(vscode, "find_editor", return_value=Path("code.cmd")):
            with self.assertRaises(ValueError):
                vscode.plan([])

    def test_open_files_starts_it_and_returns_the_editor(self) -> None:
        with mock.patch.object(vscode, "find_editor", return_value=Path("code.cmd")):
            with mock.patch.object(vscode, "_spawn") as spawn:
                editor = vscode.open_files([paths.ROOT / "a.c"])
        self.assertEqual(editor, Path("code.cmd"))
        spawn.assert_called_once()
        self.assertIn(str(paths.ROOT / "a.c"), spawn.call_args[0][0])

    def test_a_cmd_shim_goes_through_cmd_exe(self) -> None:
        # code.cmd is a batch file: without cmd.exe it is not executable, and
        # without CREATE_NO_WINDOW it flashes a console on the learner's desk.
        if not hasattr(__import__("subprocess"), "CREATE_NO_WINDOW"):
            self.skipTest("不是 Windows")
        with mock.patch("subprocess.Popen") as popen:
            vscode._spawn([str(paths.ROOT / "code.cmd"), "--reuse-window"])
        arguments = popen.call_args[0][0]
        self.assertEqual(arguments[:2], ["cmd", "/c"])
        self.assertTrue(popen.call_args[1]["creationflags"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
