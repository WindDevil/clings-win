"""The twin's curriculum difference: what it teaches, and in which order.

The topics, the exercises and their numbering are upstream's.  Two things a
learner feels are not: the order the topics are met in, and how steep each
step is.  Those are kept here, next to the Windows overrides and the
translation tables, so that ``tools/sync_from_source.py`` regenerates exactly
what learners get and ``--check`` stays the judge of the tree.

Four names carry the difference, and every one of them is applied to all three
copies of an exercise (``exercises/``, ``solutions/``, ``templates/``):

``TOPIC_ORDER``
    The order the topics are taught in.  Upstream numbers its topic
    directories in authoring order, which puts ``02_macros`` before
    ``03_types_variables``; a learner who has not met integer widths,
    signed/unsigned conversion and the usual arithmetic conversions yet meets
    ``05_x_macros`` with nothing to hang it on.  The directory names - the
    exercise ids - are left alone, because a learner's ``progress.json`` is
    keyed by them; only the order changes.

``DROPPED``
    Exercises the twin does not ship.  Each one is the later half of a pair
    that teaches the same thing twice, and the earlier half stays, so the
    ladder loses no rung and the idea is met where it first comes up.

``ADDED``
    Exercises the twin adds, kept as ordinary source files under
    ``tools/curriculum/``.  ``16_data_structures`` had three exercises that
    climbed from a ring buffer straight to a binary search tree.

``TEACHING_ORDER``
    The order inside a topic the twin has touched.  It also renumbers that
    topic, which is how a removal stops leaving a hole in the numbering, and
    rebuilds the topic page's table from the exercises themselves.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ADDITIONS = HERE / "curriculum"

# The three trees that hold one copy of every exercise.
ROLES = ("exercises", "solutions", "templates")

# The order the topics are taught in.  Upstream's own order is the numeric one
# (00_basics .. 19_modern_c_library); the only change is that the three macro
# topics of ``02_macros`` come after ``03_types_variables``.  Macro expansion,
# stringizing and ``##`` are written in terms of types and conversions, so a
# learner who has just met ``char``, ``int`` and integer promotion has
# somewhere to put them; ``02_macros/05_x_macros`` stops being a wall.
TOPIC_ORDER: tuple[str, ...] = (
    "00_basics",
    "01_preprocessor",
    "03_types_variables",
    "02_macros",
    "04_operators",
    "05_control_flow",
    "06_functions",
    "07_pointers",
    "08_arrays_strings",
    "09_dynamic_memory",
    "10_aggregates",
    "11_data_representation",
    "12_standard_library",
    "13_character_io",
    "14_file_io",
    "15_ub_safety",
    "16_data_structures",
    "17_translation_units",
    "18_advanced_c",
    "19_modern_c_library",
)

# The kept half of each duplicate pair is named in the comment: the twin drops
# the copy that repeats an idea at a worse point on the ladder, not the copy
# that introduces it.
DROPPED: dict[str, str] = {
    # 03_types_variables/03_overflow also teaches unsigned wraparound and is
    # met twenty exercises earlier, when signed overflow first matters.
    "15_ub_safety/01_signed_overflow": "03_types_variables/03_overflow",
    # 07_pointers/06_dangling_wild is the same free-then-clear through a
    # pointer-to-pointer, one topic earlier, next to the rest of the pointers.
    "15_ub_safety/04_use_after_free": "07_pointers/06_dangling_wild",
    # 07_pointers/02_null_and_const teaches the NULL check together with
    # pointer-to-const, which this exercise does not cover.
    "15_ub_safety/08_null_pointer": "07_pointers/02_null_and_const",
}

# Topics whose numbering and README the twin owns, in teaching order.  Every
# exercise of the topic has to be named here: the order is the numbering.
TEACHING_ORDER: dict[str, tuple[str, ...]] = {
    # Removals above leave 02, 03, 05.. off; renumber the survivors 01..08.
    "15_ub_safety": (
        "uninitialized",
        "out_of_bounds",
        "sequence_points",
        "strict_aliasing",
        "alignment",
        "standard_changes",
        "identifier_length",
        "implementation_defined",
    ),
    # The added stack is a smaller first step than the ring buffer, and a
    # sorted array sits between "a growable array" and "a tree that keeps
    # itself ordered": both make the climb to the tree keep its footing.
    "16_data_structures": (
        "stack_adt",
        "queue_adt",
        "dynamic_vector",
        "sorted_array_insert",
        "binary_search_tree",
    ),
}

COMMAND_LINE = re.compile(
    r"^(?P<indent>[ \t]*)(?P<launcher>\.\\clings\.cmd|\./clings) run [^\n]*$",
    re.MULTILINE,
)
TABLE_ROW = re.compile(r"^\| `[^`]+` \| .* \|$")
OBJECTIVE = re.compile(
    r"^[ \t]*\*[ \t]*objective:[ \t]*(?P<text>.*?)[ \t]*$", re.MULTILINE
)


def _stem(name: str) -> str:
    """``01_queue_adt.c`` -> ``queue_adt``; the number is not part of a name."""
    return re.sub(r"^\d+_", "", Path(name).stem)


def _names(tree: Path, role: str, topic: str) -> list[str]:
    directory = tree / role / topic
    if not directory.is_dir():
        return []
    return sorted(path.stem for path in directory.glob("*.c"))


def _touched() -> set[str]:
    topics = {ident.split("/", 1)[0] for ident in DROPPED}
    topics |= set(TEACHING_ORDER)
    for role in ROLES:
        base = ADDITIONS / role
        if not base.is_dir():
            continue
        topics |= {path.relative_to(base).parts[0] for path in base.rglob("*.c")}
    return topics


def _drop(tree: Path) -> None:
    for ident in DROPPED:
        for role in ROLES:
            path = tree / role / f"{ident}.c"
            if not path.is_file():
                raise SystemExit(f"curriculum: nothing to drop at {path}")
            path.unlink()


def _add(tree: Path) -> None:
    for role in ROLES:
        base = ADDITIONS / role
        if not base.is_dir():
            continue
        for source in sorted(base.rglob("*.c")):
            target = tree / role / source.relative_to(base)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def _teaching_order(topic: str, names: list[str]) -> list[str]:
    """The bare names of one topic, in the order they will be numbered."""
    wanted = TEACHING_ORDER.get(topic)
    if wanted is None:
        # Nothing declared: keep upstream's numbering.
        return [_stem(name) for name in names]
    present = [_stem(name) for name in names]
    if sorted(present) != sorted(wanted):
        raise SystemExit(
            f"curriculum: {topic} holds {sorted(present)}, "
            f"but TEACHING_ORDER names {sorted(wanted)}"
        )
    return list(wanted)


def _rename(tree: Path, topic: str, current: list[str], wanted: list[str]) -> None:
    """Renumber one topic in all three copies, and keep the ids in step.

    The files move by name, not by position: ``02_binary_search_tree`` becomes
    ``05_binary_search_tree`` because that is the exercise, wherever it sat in
    the old listing.
    """
    present = {_stem(name): name for name in current}
    moves = [(present[_stem(name)], name) for name in wanted]
    if all(old == new for old, new in moves):
        return
    for role in ROLES:
        directory = tree / role / topic
        # Two passes: 01->02 and 02->01 would collide in one.
        for index, (old_name, new_name) in enumerate(moves):
            if old_name != new_name:
                (directory / f"{old_name}.c").rename(
                    directory / f"{old_name}.{index}.tmp"
                )
        for index, (old_name, new_name) in enumerate(moves):
            if old_name != new_name:
                (directory / f"{old_name}.{index}.tmp").rename(
                    directory / f"{new_name}.c"
                )
    for old_name, new_name in moves:
        if old_name == new_name:
            continue
        for role in ROLES:
            path = tree / role / topic / f"{new_name}.c"
            text = path.read_text(encoding="utf-8")
            # The header comment carries the exercise id; that is the only
            # place inside a file that names it.
            text = text.replace(f"{topic}/{old_name}", f"{topic}/{new_name}")
            path.write_text(text, encoding="utf-8")


def _objective(path: Path) -> str:
    match = OBJECTIVE.search(path.read_text(encoding="utf-8"))
    if not match:
        raise SystemExit(f"curriculum: no objective line in {path}")
    return match.group("text")


def _rewrite_readme(tree: Path, topic: str, names: list[str]) -> None:
    """Point the topic page at the numbered order the learner will work in."""
    path = tree / "exercises" / topic / "README.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    rows = []
    for name in names:
        objective = _objective(tree / "exercises" / topic / f"{name}.c")
        rows.append(f"| `{name}` | {objective} |\n")
    lines = text.splitlines(keepends=True)
    first = next(
        (index for index, line in enumerate(lines) if TABLE_ROW.match(line.strip())),
        None,
    )
    if first is None:
        raise SystemExit(f"curriculum: no exercise table in {path}")
    last = first
    while last + 1 < len(lines) and TABLE_ROW.match(lines[last + 1].strip()):
        last += 1
    text = "".join(lines[:first] + rows + lines[last + 1 :])
    text = COMMAND_LINE.sub(
        lambda match: f"{match.group('indent')}{match.group('launcher')} run {names[0]}",
        text,
        count=1,
    )
    path.write_text(text, encoding="utf-8")


def apply(tree: Path) -> None:
    """Rewrite a freshly rendered tree: drop, add, renumber, fix the pages.

    Runs last in ``sync_from_source.render``, on the tree upstream plus the
    overrides and the translator produced, so it can rewrite the id lines and
    the topic pages the learner actually reads.  It is not a repair step: a
    second run complains that the exercises it drops are already gone.
    """
    _drop(tree)
    _add(tree)
    for topic in sorted(_touched()):
        current = _names(tree, "exercises", topic)
        if not current:
            raise SystemExit(f"curriculum: no exercises under {topic}")
        order = _teaching_order(topic, current)
        wanted = [f"{index:02d}_{name}" for index, name in enumerate(order, 1)]
        _rename(tree, topic, current, wanted)
        _rewrite_readme(tree, topic, wanted)


def runner_topic_order() -> str:
    """The runner's sort key, so ``clings list`` teaches in the same order."""
    entries = "".join(
        f'        "{topic}": {index},\n' for index, topic in enumerate(TOPIC_ORDER)
    )
    return (
        "    topic_order = {\n"
        + entries
        + "    }\n"
        "    exercises.sort(\n"
        "        key=lambda exercise: (\n"
        "            topic_order.get(exercise.topic, len(topic_order)),\n"
        "            exercise.slug,\n"
        "        )\n"
        "    )\n"
    )
