"""A failed run has to say what to do next, and only where a human reads it.

Every exercise starts out failing on purpose - `clings selftest` exists to
enforce exactly that - so a compiler error from `run` is the *first* thing a
learner sees, and on its own it reads like a broken installation.  The twin
prints the answer after it: the file to edit and the two commands that move
on.  These tests keep that from being quietly dropped by the next sync from
upstream, and keep it out of the machine-readable output.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
RUNNER = ROOT / "clings"
SIMPLE = "00_basics/01_printf"
# The runner prints paths the way the host spells them.
SIMPLE_FILE = str(Path("exercises") / "00_basics" / "01_printf.c")
PROJECT = "17_translation_units/02_extern_linkage"
PROJECT_TODO = str(
    Path("exercises")
    / "17_translation_units"
    / "02_extern_linkage"
    / "config.c"
)


def run_runner(
    *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RUNNER), *args],
        cwd=ROOT,
        env={**os.environ, **env} if env else None,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class TheNextStepsAfterAFailure(unittest.TestCase):
    def test_the_file_and_the_next_commands_are_named(self) -> None:
        result = run_runner("run", SIMPLE)
        if result.returncode == 0:
            self.skipTest("这个练习在这个工作区里已经做过了")
        self.assertIn("要改的文件", result.stdout)
        self.assertIn(SIMPLE_FILE, result.stdout)
        # A learner who is stuck needs both: read the hint, or just run again.
        self.assertIn(f"hint {SIMPLE}", result.stdout)
        self.assertIn(f"run {SIMPLE}", result.stdout)

    def test_the_json_output_stays_machine_readable(self) -> None:
        # The studio and every script read this; one prose line in here and
        # the menu stops being able to show anything at all.
        result = run_runner("run", SIMPLE, "--json")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["failures"], 1)
        self.assertNotIn("要改的文件", result.stdout)

    def test_a_project_names_the_file_that_contains_the_todo(self) -> None:
        result = run_runner("run", PROJECT)
        if result.returncode == 0:
            self.skipTest("这个练习在这个工作区里已经做过了")
        self.assertIn(PROJECT_TODO, result.stdout)
        self.assertNotIn(
            "要改的文件:  exercises/17_translation_units/02_extern_linkage/main.c",
            result.stdout,
        )

    def test_a_listing_does_not_lecture(self) -> None:
        result = run_runner("list")
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("要改的文件", result.stdout)


class TheMissingCompiler(unittest.TestCase):
    """The slim package's first wall: MinGW-w64 installed, but not on PATH."""

    def test_it_is_a_message_and_not_a_traceback(self) -> None:
        result = run_runner(
            "run", SIMPLE, env={"CC": "clings-no-such-compiler"}
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("没有找到 C 编译器", result.stdout)
        self.assertIn("doctor", result.stdout)
        # The learner is one compile away from the exercise, so the failure
        # must not read like a bug in clings.
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_the_same_message_covers_the_other_commands(self) -> None:
        for args in (("verify",), ("selftest",)):
            with self.subTest(args=args):
                result = run_runner(*args, env={"CC": "clings-no-such-compiler"})
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_a_broken_compiler_that_exists_is_still_a_compile_error(self) -> None:
        # CC pointing at a real program that cannot compile: that is an
        # ordinary "compilation failed", with the exercise guidance, not the
        # toolchain message.
        result = run_runner("run", SIMPLE, env={"CC": sys.executable})
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("没有找到 C 编译器", result.stdout)


class ANameThatDoesNotResolve(unittest.TestCase):
    """A typo must not read as "你全部做完了".

    resolve_exercise() answers None for two different situations, and the
    runner used to print the same green line for both - so `run 01_printf`
    (ambiguous: it matches 00_basics/01_printf and
    12_standard_library/01_printf_formats) told the learner the course was
    finished and exited 0.
    """

    def test_an_unknown_name_stops_with_a_nonzero_code(self) -> None:
        result = run_runner("run", "no_such_exercise_at_all")
        self.assertEqual(result.returncode, 1)
        self.assertIn("找不到这个练习", result.stdout)
        self.assertNotIn("所有练习都完成了", result.stdout)

    def test_an_ambiguous_name_lists_what_it_could_mean(self) -> None:
        result = run_runner("run", "01_printf")
        self.assertEqual(result.returncode, 1)
        self.assertIn("歧义", result.stdout)
        self.assertIn("00_basics/01_printf", result.stdout)
        self.assertNotIn("所有练习都完成了", result.stdout)

    def test_next_behaves_the_same_way(self) -> None:
        result = run_runner("next", "no_such_exercise_at_all")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("所有练习都完成了", result.stdout)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
