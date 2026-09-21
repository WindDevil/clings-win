"""The twin's curriculum difference: what it teaches, and in which order.

The topics, the exercises and their numbering are upstream's.  Two things a
learner feels are not: the order the topics are met in, and how steep each
step is.  Those are kept here, next to the Windows overrides and the
translation tables, so that ``tools/sync_from_source.py`` regenerates exactly
what learners get and ``--check`` stays the judge of the tree.

Five names carry the difference, and every one of them is applied to all three
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

``MOVED``
    Exercises that stay, but in a later topic.  An exercise should only ask
    for ideas already taught plus the one it introduces, and four upstream
    exercises sit earlier than an idea they need: structs before
    ``10_aggregates``, ``qsort`` and ``fgets`` before their topics, a variadic
    signature before variadic functions.  The exercise is renamed into the
    topic that teaches its last missing piece, and ``TEACHING_ORDER`` places
    it there.

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
    # Aggregates come before the topics that build on them: compound literals,
    # flexible array members, linked lists and the arena all speak in structs.
    "10_aggregates",
    "08_arrays_strings",
    "09_dynamic_memory",
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
    # fopen, fputs and fread are 14_file_io's subject, taught there across
    # four exercises that build on each other; this one runs the same
    # introduction one topic earlier, before 13_character_io has even run.
    "12_standard_library/07_file_io": "14_file_io/01_fprintf_fscanf",
    # "Include the header that declares the function you call" is
    # 00_basics/07_include_header and 01_preprocessor/01_include_standard;
    # after ctype_full has run (12_standard_library), this asks it again.
    "13_character_io/06_include_ctypes": "12_standard_library/13_ctype_full",
}

# Exercises that stay, but in a later topic, keyed by bare name: the number
# is the twin's to assign, so TEACHING_ORDER of the receiving topic names the
# exercise where the learner will meet it.  Each one sat earlier than an idea
# it cannot work without.
MOVED: dict[str, str] = {
    # fwrite/fread of a struct is 14_file_io's subject, and binary mode is
    # 06_binary_random_access there; in 10_aggregates both were still ahead.
    "10_aggregates/struct_file": "14_file_io",
    # The sort is qsort (12_standard_library/03) over lines read with fgets
    # (14_file_io/02); as an 08_arrays_strings exercise it asked for both
    # before either topic.
    "08_arrays_strings/fgets_fputs_sort": "14_file_io",
    # An X-macro's payload here is an enum plus a table of strings: enum is
    # 10_aggregates/06 and string tables are 08_arrays_strings.  At the end of
    # 08 both are in hand; in 02_macros neither was.
    "02_macros/x_macros": "08_arrays_strings",
    # Default argument promotions only happen at a variadic call, and the
    # variadic machinery the exercise is written in is 18_advanced_c/01.
    "12_standard_library/default_argument_promotions": "18_advanced_c",
}

# Topics whose numbering and README the twin owns, in teaching order.  Every
# exercise of the topic has to be named here: the order is the numbering.
TEACHING_ORDER: dict[str, tuple[str, ...]] = {
    # x_macros left for 08_arrays_strings; the rest close ranks.
    "02_macros": (
        "object_macro",
        "function_macro",
        "stringize_paste",
        "variadic_macros",
        "macro_whitespace",
        "macro_statement",
        "macro_not_typedef",
        "macro_side_effects",
        "assert_macro",
        "macro_multiline",
    ),
    # fgets_fputs_sort left for 14_file_io; x_macros arrives from 02_macros
    # as the topic's closing exercise, once enums and string tables exist.
    "08_arrays_strings": (
        "array_basics",
        "array_decay",
        "multidimensional",
        "string_literals",
        "string_ops",
        "tokenize",
        "vla",
        "compound_literals",
        "pointer_compatibility",
        "asymmetric_bounds",
        "strcat_strncat",
        "strncpy_bounded",
        "sprintf_snprintf",
        "strtod",
        "main_args",
        "state_machine",
        "escaped_strings",
        "x_macros",
    ),
    # struct_file left for 14_file_io; the rest keep their order.
    "10_aggregates": (
        "struct_basics",
        "nested_structs",
        "padding_alignment",
        "bitfields",
        "union",
        "enum",
        "typedef_designated",
        "container_of",
        "struct_array",
        "struct_pass",
        "complex_declarations",
        "declaration_grammar",
    ),
    # file_io is dropped (14_file_io teaches it) and
    # default_argument_promotions moved to 18_advanced_c.
    "12_standard_library": (
        "printf_formats",
        "strtol_errno",
        "qsort_bsearch",
        "math_functions",
        "time_functions",
        "random",
        "memory_functions",
        "string_search",
        "stdint_inttypes",
        "environment",
        "printf_advanced",
        "scanf_advanced",
        "ctype_full",
        "rand_max",
    ),
    # include_ctypes is dropped: the include lesson was taught in 00_basics
    # and 01_preprocessor, and ctype itself in 12_standard_library/13.
    "13_character_io": (
        "getc_putc",
        "eof_ferror",
        "input_validation",
        "iso646",
        "getchar_putchar",
    ),
    # fgets_fputs_sort arrives once fgets is taught; struct_file closes the
    # topic, a binary fwrite/fread with everything else already met.
    "14_file_io": (
        "fprintf_fscanf",
        "fgets_fputs",
        "fgets_fputs_sort",
        "getc_putc_ungetc",
        "fseek_ftell",
        "fflush_setvbuf",
        "binary_random_access",
        "buffered_output_memory",
        "struct_file",
    ),
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
    # default_argument_promotions arrives from 12_standard_library: it is the
    # variadic exercise's immediate successor, because a variadic call is the
    # only place the promotions happen.
    "18_advanced_c": (
        "variadic",
        "default_argument_promotions",
        "setjmp_longjmp",
        "pthreads",
        "atomics",
        "generic",
        "static_assert",
        "align",
        "anonymous_union",
        "thread_local",
        "complex",
        "signal",
        "stack_frame",
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
    topics |= {ident.split("/", 1)[0] for ident in MOVED}
    topics |= set(MOVED.values())
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


def _move(tree: Path) -> None:
    """Carry each MOVED exercise into its new topic, in all three copies.

    Runs before the renumbering: the file still wears its upstream number,
    which the receiving topic's TEACHING_ORDER then replaces.  The header
    comment's id line is the only place inside a file that names it, so the
    topic half of the id is rewritten here and the number half there.
    """
    for ident, target in MOVED.items():
        source_topic, name = ident.split("/", 1)
        for role in ROLES:
            directory = tree / role / source_topic
            matches = list(directory.glob(f"*_{name}.c"))
            if len(matches) != 1:
                raise SystemExit(
                    f"curriculum: expected one {name} under {directory}, "
                    f"found {len(matches)}"
                )
            path = matches[0]
            text = path.read_text(encoding="utf-8")
            text = text.replace(
                f"{source_topic}/{path.stem}", f"{target}/{path.stem}"
            )
            path.write_text(text, encoding="utf-8")
            path.rename(tree / role / target / path.name)


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
    _move(tree)
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
