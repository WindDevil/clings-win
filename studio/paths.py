"""Which files the studio is allowed to touch.

A local web server that writes files needs one place that decides what "a
file" means, and this is it.  The rule is deliberately narrow: a request may
name only the files the runner listed as belonging to one exercise, resolved,
so no amount of ``..``, an absolute path, or a symlink can reach anything
else in the package - or outside it.

The exercise list is the source of truth for what belongs to an exercise, so
this module needs a Listing to answer.  It never invents a path from a name.
"""

from __future__ import annotations

from pathlib import Path

from .bridge import Exercise, Listing

ROOT = Path(__file__).resolve().parent.parent


class PathNotAllowed(ValueError):
    """A request named a file that is not part of the exercise."""


def resolve_within(base: Path, relative: str) -> Path:
    """Join *relative* onto *base*, refusing anything that escapes it.

    resolve() is what does the work: it collapses "..", follows symlinks, and
    normalises case on Windows, so the containment check afterwards compares
    two real locations rather than two spellings.
    """
    base = base.resolve()
    candidate = (base / relative).resolve()
    if candidate != base and base not in candidate.parents:
        raise PathNotAllowed(f"越界路径: {relative}")
    return candidate


def exercise_files(exercise: Exercise) -> tuple[Path, ...]:
    """Every file of one exercise, resolved under this package's root."""
    files = []
    for relative in exercise.files:
        try:
            files.append(resolve_within(ROOT, relative))
        except PathNotAllowed:
            continue
    return tuple(files)


def find_file(listing: Listing, exercise: Exercise, name: str) -> Path:
    """Resolve *name* to a file of *exercise*, or raise PathNotAllowed.

    *name* may be the relative path the runner reported, or an absolute path
    inside the same directory; both are reduced to the same comparison.
    """
    allowed = exercise_files(exercise)
    if not allowed:
        raise PathNotAllowed(f"{exercise.ident} 没有可编辑的文件")

    given = Path(name)
    target = given.resolve() if given.is_absolute() else resolve_within(ROOT, name)
    for candidate in allowed:
        if candidate == target:
            return candidate
    raise PathNotAllowed(f"{name} 不属于 {exercise.ident}")


def relative(path: Path) -> str:
    """A path as the JSON interface spells it: package-relative, "/" separated."""
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def is_editable(path: Path) -> bool:
    """Whether saving this file would survive the next `make sync`.

    Everything under exercises/ is the learner's.  A topic README.md is
    generated from upstream like the exercises themselves, so it is shown
    read-only rather than letting an edit vanish silently.
    """
    name = path.name.lower()
    if name == "readme.md":
        return False
    return path.suffix.lower() in {".c", ".h"}
