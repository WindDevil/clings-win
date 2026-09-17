"""The web server: a local server that writes files, so its edges matter.

Two kinds of claim are checked here.

Narrow: what the page is allowed to reach.  A browser on the learner's machine
is the only thing that can read the token, and a request that names a file
outside the one exercise it belongs to is refused however it is spelled.  The
server is bound to 127.0.0.1 and anyone at the keyboard can already edit these
files, so this is not a defence against the learner - it is a defence against
every other page in their browser, which is a real thing that visits
localhost.

Wide: the contract with the runner.  The page's whole view of the exercises
comes through these endpoints, and `run` is where a saved file becomes a
result.  Those tests use the real runner and the real compiler; the ones that
would move the learner's exercises put every byte back.
"""

from __future__ import annotations

import contextlib
import unittest

from .. import paths
from ..server import MAX_BODY
from . import harness
from .harness import NO_SEMICOLON, ServerCase, solution

SIMPLE = "00_basics/01_printf"
SIMPLE_FILE = f"exercises/{SIMPLE}.c"
# Reads the keyboard, so it can prove stdin reaches the compiled program.
STDIN_EXERCISE = "13_character_io/05_getchar_putchar"
STDIN_FILE = f"exercises/{STDIN_EXERCISE}.c"


class ThePage(ServerCase):
    def test_it_is_served_with_the_token_and_a_policy(self) -> None:
        response = self.server.request("GET", "/")
        self.assertEqual(response.status, 200)
        self.assertIn("text/html", response.headers["Content-Type"])
        self.assertNotIn("__CLINGS_TOKEN__", response.payload)
        self.assertIn(self.server.token, response.payload)
        policy = response.headers["Content-Security-Policy"]
        # No inline script: the README the page renders is upstream's text,
        # and a policy that let it run would be a policy that runs whatever
        # the exercises ever contain.
        self.assertIn("script-src 'self'", policy)
        self.assertNotIn("unsafe-eval", policy)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

    def test_nothing_is_cached(self) -> None:
        response = self.server.request("GET", "/")
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_unknown_pages_are_404(self) -> None:
        self.assertEqual(self.server.request("GET", "/nope").status, 404)

    def test_favicon_is_answered_without_a_body(self) -> None:
        self.assertEqual(self.server.request("GET", "/favicon.ico").status, 204)


class StaticFiles(ServerCase):
    def test_the_editor_assets_are_served(self) -> None:
        for route, expected in (
            ("/static/app.js", "javascript"),
            ("/static/ui.css", "css"),
            ("/static/vendor/codemirror/lib/codemirror.js", "javascript"),
            ("/static/vendor/codemirror/mode/clike/clike.js", "javascript"),
            ("/static/vendor/marked/marked.min.js", "javascript"),
        ):
            with self.subTest(route=route):
                response = self.server.request("GET", route)
                self.assertEqual(response.status, 200)
                self.assertIn(expected, response.headers["Content-Type"])

    def test_a_missing_asset_is_404(self) -> None:
        self.assertEqual(self.server.request("GET", "/static/nope.js").status, 404)

    def test_static_files_cannot_escape_their_directory(self) -> None:
        # The same rule as for exercise files, on the other directory: the
        # assets are the only thing under /static/.
        for route in (
            "/static/../server.py",
            "/static/../../clings",
            "/static/..%2f..%2fclings",
        ):
            with self.subTest(route=route):
                self.assertIn(
                    self.server.request("GET", route).status, (403, 404)
                )


class Authorisation(ServerCase):
    """Only the page we served may talk to the API."""

    def test_without_the_token(self) -> None:
        self.assertEqual(
            self.server.request("GET", "/api/session", token=False).status, 403
        )

    def test_with_the_wrong_token(self) -> None:
        response = self.server.request(
            "GET", "/api/session?token=not-the-token", token=False
        )
        self.assertEqual(response.status, 403)

    def test_from_another_origin(self) -> None:
        # What a form on some other site would send.
        response = self.server.request(
            "GET", "/api/session", origin="http://evil.example"
        )
        self.assertEqual(response.status, 403)

    def test_our_own_origin_and_token_is_enough(self) -> None:
        response = self.server.request("GET", "/api/session", origin=self.server.state.origin)
        self.assertEqual(response.status, 200)

    def test_the_token_may_come_in_the_query(self) -> None:
        # EventSource cannot set a header; nothing uses it yet, but the path
        # is part of what _authorised() promises.
        response = self.server.request(
            "GET", f"/api/session?token={self.server.token}", token=False
        )
        self.assertEqual(response.status, 200)


class SessionAndListing(ServerCase):
    def test_the_session_describes_the_package(self) -> None:
        payload = self.server.request("GET", "/api/session").payload
        self.assertEqual(payload["total"], harness.listing().total)
        self.assertGreater(payload["total"], 0)
        by_id = {item["id"]: item for item in payload["languages"]}
        self.assertIn("c", by_id)
        self.assertTrue(by_id["c"]["checks"])
        # The fallback language has to be advertised too: a file nobody claims
        # is still openable.
        self.assertIn("plain", by_id)
        self.assertFalse(by_id["plain"]["checks"])
        self.assertIn("compiler", payload["toolchain"])

    def test_every_exercise_is_listed_with_its_files(self) -> None:
        payload = self.server.request("GET", "/api/exercises").payload
        self.assertEqual(payload["total"], harness.listing().total)
        idents = [
            item["ident"]
            for topic in payload["topics"]
            for item in topic["exercises"]
        ]
        self.assertEqual(len(idents), payload["total"])
        self.assertEqual(len(idents), len(set(idents)))
        for topic in payload["topics"]:
            for item in topic["exercises"]:
                self.assertTrue(item["files"], f"{item['ident']} 没有文件")
                self.assertTrue(item["title"])

    def test_one_exercise_comes_with_its_neighbours(self) -> None:
        payload = self.server.request("GET", f"/api/exercise/{SIMPLE}").payload
        self.assertEqual(payload["exercise"]["ident"], SIMPLE)
        self.assertTrue(payload["exercise"]["objective"])
        files = {item["path"]: item for item in payload["files"]}
        self.assertIn(SIMPLE_FILE, files)
        self.assertTrue(files[SIMPLE_FILE]["editable"])
        self.assertEqual(files[SIMPLE_FILE]["language_id"], "c")
        order = [item.ident for item in harness.listing().exercises]
        index = order.index(SIMPLE)
        self.assertEqual(payload["previous"], order[index - 1] if index else "")
        self.assertEqual(payload["next"], order[index + 1])

    def test_the_topics_readme_comes_along_read_only(self) -> None:
        payload = self.server.request("GET", f"/api/exercise/{SIMPLE}").payload
        readme = payload["topic_readme"]
        self.assertTrue(readme["exists"])
        self.assertTrue(readme["path"].startswith("exercises/"))
        self.assertTrue(readme["path"].endswith("README.md"))
        self.assertTrue(readme["content"].strip())
        # Read-only is the point: it comes alongside the editable files rather
        # than among them, because an edit would vanish at the next sync.
        for item in payload["files"]:
            self.assertNotEqual(item["path"], readme["path"])

    def test_an_ambiguous_name_is_reported_with_the_candidates(self) -> None:
        # Deliberately the same resolution the runner uses, so a name the
        # editor accepts is never one `clings run` would refuse.
        payload = self.server.request("GET", "/api/exercise/01_printf").payload
        self.assertIn("candidates", payload)
        self.assertGreater(len(payload["candidates"]), 1)
        self.assertIn(SIMPLE, payload["candidates"])

    def test_an_unknown_name_is_404(self) -> None:
        self.assertEqual(
            self.server.request("GET", "/api/exercise/no_such_exercise").status, 404
        )


class ReadingFiles(ServerCase):
    def test_a_file_comes_with_a_revision(self) -> None:
        payload = self.server.request("GET", f"/api/file?path={SIMPLE_FILE}").payload
        self.assertEqual(payload["path"], SIMPLE_FILE)
        self.assertTrue(payload["content"])
        self.assertTrue(payload["revision"])
        self.assertTrue(payload["editable"])
        self.assertEqual(payload["language_id"], "c")

    def test_a_file_without_an_exercise_is_refused(self) -> None:
        for name in ("exercises/README.md", "clings.cmd", "include/clings/test.h"):
            with self.subTest(name=name):
                self.assertEqual(
                    self.server.request("GET", f"/api/file?path={name}").status, 403
                )

    def test_paths_outside_the_package_are_refused(self) -> None:
        for name in ("../../etc/passwd", "..%2f..%2fetc%2fpasswd", "D:/Windows/win.ini"):
            with self.subTest(name=name):
                self.assertIn(
                    self.server.request("GET", f"/api/file?path={name}").status,
                    (403, 404),
                )

    def test_the_path_parameter_is_required(self) -> None:
        self.assertEqual(self.server.request("GET", "/api/file").status, 400)


class WritingFiles(ServerCase):
    """Saving is the one thing here that destroys something."""

    def read(self, name: str = SIMPLE_FILE):
        return self.server.request("GET", f"/api/file?path={name}").payload

    def test_saving_the_same_text_is_allowed(self) -> None:
        current = self.read()
        with harness.unchanged(paths.ROOT / SIMPLE_FILE):
            response = self.server.request(
                "PUT",
                "/api/file",
                {
                    "path": SIMPLE_FILE,
                    "content": current["content"],
                    "base_revision": current["revision"],
                },
            )
        self.assertEqual(response.status, 200)
        self.assertEqual(response.payload["revision"], current["revision"])

    def test_a_stale_revision_is_refused_and_answered_with_the_new_text(self) -> None:
        # The case this exists for: the answer was applied in another window
        # while this one had the file open.  Saving would silently undo it.
        target = paths.ROOT / SIMPLE_FILE
        with harness.unchanged(target):
            response = self.server.request(
                "PUT",
                "/api/file",
                {
                    "path": SIMPLE_FILE,
                    "content": "/* overwritten */\n",
                    "base_revision": "0000000000000000",
                },
            )
            self.assertEqual(response.status, 409)
            self.assertTrue(response.payload["conflict"])
            self.assertEqual(response.payload["content"], target.read_text(encoding="utf-8"))
            self.assertNotIn("overwritten", target.read_text(encoding="utf-8"))

    def test_a_read_only_file_cannot_be_written(self) -> None:
        response = self.server.request(
            "PUT", "/api/file", {"path": "exercises/00_basics/README.md", "content": "x"}
        )
        self.assertEqual(response.status, 403)

    def test_a_file_outside_the_package_cannot_be_written(self) -> None:
        response = self.server.request(
            "PUT", "/api/file", {"path": "../escape.c", "content": "x"}
        )
        self.assertEqual(response.status, 403)

    def test_the_body_has_to_be_a_json_object(self) -> None:
        self.assertEqual(
            self.server.request("PUT", "/api/file", raw=b"not json").status, 400
        )
        self.assertEqual(
            self.server.request("PUT", "/api/file", raw=b"[1, 2, 3]").status, 400
        )

    def test_a_body_larger_than_the_limit_is_refused(self) -> None:
        response = self.server.request(
            "PUT",
            "/api/file",
            raw=b'{"path": "x", "content": "' + b"a" * (MAX_BODY + 100) + b'"}',
        )
        self.assertEqual(response.status, 413)

    def test_missing_fields_are_a_bad_request(self) -> None:
        self.assertEqual(
            self.server.request("PUT", "/api/file", {"path": SIMPLE_FILE}).status, 400
        )
        self.assertEqual(self.server.request("PUT", "/api/file", {}).status, 400)


class UnknownEndpoints(ServerCase):
    def test_unknown_api_routes_are_404(self) -> None:
        self.assertEqual(self.server.request("GET", "/api/nope").status, 404)
        self.assertEqual(self.server.request("POST", "/api/nope", {}).status, 404)
        self.assertEqual(self.server.request("PUT", "/api/nope", {}).status, 404)


class Running(ServerCase):
    """`run`: a saved file, the compiler, and the checks."""

    def unsolved(self) -> str:
        """The next exercise the learner has not passed.

        Read from progress rather than named here: whether a given exercise is
        solved is the learner's business, and a test that assumed a particular
        answer would fail on their machine for no good reason.
        """
        found = harness.listing().next_exercise()
        if found is None:
            self.skipTest("这个包里的练习都做完了")
        return found.ident

    def test_an_unsolved_exercise_fails_its_checks(self) -> None:
        ident = self.unsolved()
        target = harness.files_of(ident)[0]
        before = target.read_bytes()
        response = self.server.request("POST", "/api/run", {"ident": ident})
        self.assertEqual(response.status, 200)
        result = response.payload["result"]
        self.assertEqual(result["ident"], ident)
        self.assertIn(result["stage"], ("compile", "run"))
        self.assertFalse(result["passed"])
        self.assertTrue(result["stage_label"])
        self.assertTrue(result["output"].strip())
        # Running compiles; it must not edit.  A learner's file is theirs.
        self.assertEqual(target.read_bytes(), before)

    def test_the_counts_come_back_for_the_progress_bar(self) -> None:
        payload = self.server.request(
            "POST", "/api/run", {"ident": self.unsolved()}
        ).payload
        self.assertEqual(payload["total"], harness.listing().total)
        self.assertIsInstance(payload["completed_count"], int)
        self.assertIsInstance(payload["next"], str)

    def test_a_compile_failure_comes_back_as_diagnostics(self) -> None:
        # A build that fails is the editor's business, so the page gets the
        # same shape /api/check would have given it.  The text is broken on
        # purpose, and put back before this test returns.
        ident = self.unsolved()
        target = harness.files_of(ident)[0]
        with harness.unchanged(target):
            target.write_text(NO_SEMICOLON, encoding="utf-8")
            response = self.server.request("POST", "/api/run", {"ident": ident})
            self.assertEqual(response.status, 200)
            result = response.payload["result"]
            self.assertEqual(result["stage"], "compile")
            self.assertFalse(result["passed"])
            diagnostics = response.payload["diagnostics"]
            self.assertTrue(diagnostics, "编译失败却没有给出诊断")
            self.assertEqual(diagnostics[0]["file"], paths.relative(target))
            self.assertIn("error", {item["severity"] for item in diagnostics})

    def test_an_ambiguous_name_is_refused(self) -> None:
        response = self.server.request("POST", "/api/run", {"ident": "01_printf"})
        self.assertEqual(response.status, 409)
        self.assertTrue(response.payload["candidates"])

    def test_an_unknown_name_is_404(self) -> None:
        self.assertEqual(
            self.server.request("POST", "/api/run", {"ident": "nope"}).status, 404
        )

    def test_ident_is_required_and_stdin_has_to_be_text(self) -> None:
        self.assertEqual(self.server.request("POST", "/api/run", {}).status, 400)
        self.assertEqual(
            self.server.request(
                "POST", "/api/run", {"ident": SIMPLE, "stdin": 5}
            ).status,
            400,
        )


@unittest.skipUnless(harness.compiler_ready(), "没有编译器")
class Checking(ServerCase):
    """`check`: the editor's live diagnostics."""

    def body(self, content: str, name: str = SIMPLE_FILE):
        return {"path": name, "content": content}

    def test_a_clean_buffer_has_no_diagnostics(self) -> None:

        payload = self.server.request(
            "POST", "/api/check", self.body(solution(SIMPLE))
        ).payload
        self.assertEqual(payload["diagnostics"], [])
        self.assertEqual(payload["path"], SIMPLE_FILE)

    def test_a_broken_buffer_comes_back_in_editor_shape(self) -> None:

        payload = self.server.request(
            "POST", "/api/check", self.body(solution(SIMPLE) + NO_SEMICOLON)
        ).payload
        self.assertTrue(payload["diagnostics"])
        first = payload["diagnostics"][0]
        for key in ("line", "column", "severity", "message", "file", "code", "context"):
            self.assertIn(key, first)
        self.assertEqual(first["file"], SIMPLE_FILE)
        self.assertIsInstance(first["line"], int)

    def test_a_file_without_an_exercise_is_refused(self) -> None:
        response = self.server.request(
            "POST", "/api/check", self.body("x", "exercises/README.md")
        )
        self.assertEqual(response.status, 403)

    def test_missing_fields_are_a_bad_request(self) -> None:
        self.assertEqual(
            self.server.request("POST", "/api/check", {"path": SIMPLE_FILE}).status, 400
        )


@unittest.skipUnless(harness.compiler_ready(), "没有编译器")
class Completion(ServerCase):
    def test_it_offers_the_library_and_the_exercise(self) -> None:
        # An empty buffer, so nothing local shadows the snippet below.
        payload = self.server.request(
            "POST",
            "/api/completion",
            {"path": SIMPLE_FILE, "content": ""},
        ).payload
        items = {item["label"]: item for item in payload["items"]}
        self.assertIn("printf", items)
        self.assertEqual(items["printf"]["header"], "<stdio.h>")
        # The insert text is what the editor pastes, and it is not always the
        # label: a snippet pastes a body.
        self.assertIn("int main", items["main"]["insert"])

    def test_a_file_without_an_exercise_is_refused(self) -> None:
        response = self.server.request(
            "POST",
            "/api/completion",
            {"path": "exercises/README.md", "content": "x"},
        )
        self.assertEqual(response.status, 403)


class SolutionsAndResets(ServerCase):
    def test_the_reference_answer_is_readable(self) -> None:
        payload = self.server.request(
            "POST", "/api/solution", {"ident": SIMPLE}
        ).payload
        self.assertIn("print_greeting", payload["text"])
        self.assertNotIn("TODO", payload["text"])

    def test_an_unknown_exercise_is_404(self) -> None:
        self.assertEqual(
            self.server.request(
                "POST", "/api/solution", {"ident": "nope"}
            ).status,
            404,
        )
        self.assertEqual(
            self.server.request("POST", "/api/reset", {"ident": "nope"}).status, 404
        )

    def test_ident_is_required(self) -> None:
        self.assertEqual(self.server.request("POST", "/api/reset", {}).status, 400)


@unittest.skipUnless(harness.compiler_ready(), "没有编译器")
class TheWholeLoop(ServerCase):
    """Apply, run, reset - the three things that change the learner's files.

    Everything this touches is put back in tearDown, because a test that
    leaves a solved exercise behind would be a test that lies about the next
    run of the suite.
    """

    def setUp(self) -> None:
        super().setUp()
        self.target = paths.ROOT / STDIN_FILE
        # Byte for byte, and progress too: a pass is recorded outside the file,
        # so restoring the exercise is not enough on its own.
        self.restore = contextlib.ExitStack()
        self.addCleanup(self.restore.close)
        self.restore.enter_context(
            harness.unchanged(self.target, harness.PROGRESS)
        )

    def test_apply_run_with_input_then_reset(self) -> None:
        original = self.target.read_text(encoding="utf-8")

        applied = self.server.request(
            "POST", "/api/solution", {"ident": STDIN_EXERCISE, "apply": True}
        )
        self.assertEqual(applied.status, 200)
        self.assertEqual(applied.payload["action"], "solution")
        solved = self.target.read_text(encoding="utf-8")
        self.assertNotEqual(solved, original, "参考答案没有写进去")

        # stdin is the reason this exercise was picked: without it the program
        # would block on a read that can never arrive, and the run would be a
        # timeout rather than a pass.
        response = self.server.request(
            "POST", "/api/run", {"ident": STDIN_EXERCISE, "stdin": "abc\n"}
        )
        result = response.payload["result"]
        self.assertTrue(
            result["passed"], f"套用了参考答案却没通过: {result['output'][:400]}"
        )
        self.assertEqual(result["stage"], "run")

        reset = self.server.request("POST", "/api/reset", {"ident": STDIN_EXERCISE})
        self.assertEqual(reset.status, 200)
        self.assertEqual(reset.payload["action"], "reset")
        self.assertEqual(self.target.read_text(encoding="utf-8"), original)

    def test_reset_puts_an_exercise_back(self) -> None:
        # Reset works on an exercise nobody has touched, which is also the
        # path someone takes to start over.
        before = self.target.read_text(encoding="utf-8")
        response = self.server.request("POST", "/api/reset", {"ident": STDIN_EXERCISE})
        self.assertEqual(response.status, 200)
        self.assertEqual(self.target.read_text(encoding="utf-8"), before)


class OpeningInVsCode(ServerCase):
    def test_it_reports_an_editor_or_says_there_is_none(self) -> None:
        # No window may open during a test run, so the spawn is intercepted;
        # what is under test is the answer the page gets back.
        from unittest import mock

        from .. import vscode

        with mock.patch.object(vscode, "_spawn", return_value=None) as spawn:
            with mock.patch.object(vscode, "find_editor", return_value=None):
                missing = self.server.request(
                    "POST", "/api/open-vscode", {"ident": SIMPLE}
                )
                self.assertEqual(missing.status, 424)
                self.assertIn("web", missing.payload["error"])
            spawn.assert_not_called()

            with mock.patch.object(
                vscode, "find_editor", return_value=paths.ROOT / "code.cmd"
            ):
                found = self.server.request("POST", "/api/open-vscode", {"ident": SIMPLE})
                self.assertEqual(found.status, 200)
                self.assertEqual(found.payload["path"], SIMPLE_FILE)
            # One launch, one window: the folder is the workspace.
            spawn.assert_called_once()
            arguments = spawn.call_args[0][0]
            self.assertIn("--reuse-window", arguments)
            self.assertIn(str(paths.ROOT), arguments)

    def test_ident_is_required(self) -> None:
        self.assertEqual(
            self.server.request("POST", "/api/open-vscode", {}).status, 400
        )
