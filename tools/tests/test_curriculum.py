"""The twin's curriculum difference has to keep describing the tree.

tools/curriculum.py renames files and rewrites the topic pages, so a slip there
is a learner opening the file for one exercise and finding another - which is
exactly what a first cut of the renumbering did.  These tests pin what it
promises: the runner teaches the topics in the declared order, the duplicates
are gone in every copy while the exercise that introduces the idea stays, and
each renumbered topic counts 01..N in the order its own page lists.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))

import curriculum  # noqa: E402

ROOT = TOOLS.parent
TABLE_ROW = re.compile(r"^\| `([^`]+)` \| .* \|$")


def numbers(topic: str, role: str) -> list[str]:
    return sorted(path.stem for path in (ROOT / role / topic).glob("*.c"))


def body(path: Path) -> str:
    """A file without its id line: the tree numbers that, the source does not."""
    return "".join(
        line
        for line in path.read_text("utf-8").splitlines(keepends=True)
        if "clings 练习:" not in line
    )


class TheCurriculum(unittest.TestCase):
    def test_every_topic_has_a_place_in_the_order(self) -> None:
        topics = {path.parent.name for path in (ROOT / "exercises").glob("*/*.c")}
        topics |= {
            path.parent.parent.name
            for path in (ROOT / "exercises").glob("*/*/main.c")
        }
        # An upstream topic the twin has not placed would sort to the end, and
        # the order the learner gets would depend on nothing at all.
        self.assertEqual(sorted(topics - set(curriculum.TOPIC_ORDER)), [])

    def test_a_dropped_exercise_is_gone_from_every_copy(self) -> None:
        for ident, kept in curriculum.DROPPED.items():
            with self.subTest(ident=ident):
                # The exercise that introduces the idea stays, so the ladder
                # keeps its rung; the repeat and all three of its copies go,
                # or `solution` and `reset` would still answer for it.
                self.assertTrue((ROOT / "exercises" / f"{kept}.c").is_file())
                for role in curriculum.ROLES:
                    self.assertFalse((ROOT / role / f"{ident}.c").exists())

    def test_a_renumbered_topic_counts_from_one_in_teaching_order(self) -> None:
        for topic, order in curriculum.TEACHING_ORDER.items():
            wanted = [f"{index:02d}_{stem}" for index, stem in enumerate(order, 1)]
            for role in curriculum.ROLES:
                with self.subTest(topic=topic, role=role):
                    self.assertEqual(numbers(topic, role), wanted)

    def test_the_topic_page_lists_them_in_that_order(self) -> None:
        for topic in curriculum.TEACHING_ORDER:
            page = (ROOT / "exercises" / topic / "README.md").read_text("utf-8")
            listed = []
            for line in page.splitlines():
                match = TABLE_ROW.match(line.strip())
                if match:
                    listed.append(match.group(1))
            names = numbers(topic, "exercises")
            self.assertEqual(listed, names)
            # The command the page hands a beginner has to be the first one.
            self.assertIn(f"run {names[0]}", page)

    def test_an_added_exercise_reaches_all_three_trees(self) -> None:
        """The copy in the tree is the source, plus the number of the day."""
        for role in curriculum.ROLES:
            base = curriculum.ADDITIONS / role
            if not base.is_dir():
                continue
            for source in sorted(base.rglob("*.c")):
                relative = source.relative_to(base)
                with self.subTest(source=relative):
                    found = list(
                        (ROOT / role / relative.parent).glob(f"*_{relative.stem}.c")
                    )
                    self.assertEqual(len(found), 1)
                    self.assertEqual(body(found[0]), body(source))

    def test_the_runner_lists_the_topics_in_the_same_order(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "clings"), "list", "--json"],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            check=True,
        )
        listed = [topic["name"] for topic in json.loads(result.stdout)["topics"]]
        self.assertEqual(listed, list(curriculum.TOPIC_ORDER))


if __name__ == "__main__":
    unittest.main()
