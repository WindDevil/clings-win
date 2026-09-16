#!/usr/bin/env python3
"""Translate the generated tree with the tables in tools/zh_glossary.py.

Runs as the last step of ``make sync``, after the Windows overrides, so the
exercise files that learners open are Chinese while identifiers, API names and
format specifiers stay English.

Any English text without an entry is reported.  ``--strict`` (what sync and CI
use) turns that report into a failure, so an upstream text change shows up as a
build error instead of silently leaving half a comment in English.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zh_glossary import COMMENTS, HINTS, LINES, OBJECTIVES, TITLES  # noqa: E402

FIELDS = {"title": TITLES, "objective": OBJECTIVES, "hint": HINTS}

SOURCE_SUFFIXES = (".c", ".h")
MARKDOWN_DIR = "exercises"

CJK = re.compile(r"[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]")
FIELD_LINE = re.compile(r"^(title|objective|hint): (.*)$")
EXERCISE_LINE = re.compile(r"^clings exercise: (.*)$")
README_TABLE_ROW = re.compile(r"^\| `([^`]+)` \| (.*) \|$")


class Report:
    def __init__(self) -> None:
        self.missing: dict[str, list[str]] = {}
        self.translated = 0

    def add(self, where: str, text: str) -> None:
        self.missing.setdefault(where, []).append(text)

    def count(self, amount: int = 1) -> None:
        self.translated += amount


def has_chinese(text: str) -> bool:
    return bool(CJK.search(text))


def translate_comment_text(text: str, report: Report, where: str) -> str:
    """Translate one comment/metadata payload, keeping its shape."""
    if not text or has_chinese(text):
        return text

    exercise = EXERCISE_LINE.match(text)
    if exercise:
        report.count()
        return f"clings 练习: {exercise.group(1)}"

    field = FIELD_LINE.match(text)
    if field:
        table = FIELDS[field.group(1)]
        value = field.group(2)
        if value in table:
            report.count()
            return f"{field.group(1)}: {table[value]}"
        report.add(where, value)
        return text

    if text in COMMENTS:
        report.count()
        return COMMENTS[text]

    report.add(where, text)
    return text


def translate_source(path: Path, report: Report) -> str:
    """Rewrite the comments of one C source or header."""
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    output: list[str] = []
    in_block = False

    for line in lines:
        newline = ""
        body = line
        if body.endswith("\n"):
            body, newline = body[:-1], "\n"

        stripped = body.strip()
        where = f"{path}: {stripped[:60]}"

        if stripped in LINES:
            output.append(LINES[stripped] + newline)
            report.count()
            continue

        if in_block:
            # Comment continuation: " * text", " *", " */".
            if stripped in ("*/", "* /", "*"):
                in_block = not stripped.endswith("*/")
                output.append(body + newline)
                continue
            match = re.match(r"^(\s*\*)( ?)(.*?)(\s*)$", body)
            if match and "*/" not in match.group(3):
                prefix, space, content, padding = match.groups()
                translated = translate_comment_text(content, report, where)
                output.append(f"{prefix}{space}{translated}{padding}{newline}")
                if stripped.endswith("*/"):
                    in_block = False
                continue
            in_block = False

        if stripped.startswith("/*"):
            if stripped.endswith("*/") and stripped.count("*/") == 1:
                inner = stripped[2:-2].strip()
                translated = translate_comment_text(inner, report, where)
                leading = body[: len(body) - len(body.lstrip())]
                output.append(f"{leading}/* {translated} */{newline}")
                continue
            in_block = True
            if stripped != "/*":
                inner = stripped[2:].strip()
                translated = translate_comment_text(inner, report, where)
                leading = body[: len(body) - len(body.lstrip())]
                output.append(f"{leading}/* {translated}{newline}")
                continue
            output.append(body + newline)
            continue

        if stripped.startswith("//"):
            inner = stripped[2:].strip()
            translated = translate_comment_text(inner, report, where)
            leading = body[: len(body) - len(body.lstrip())]
            output.append(f"{leading}// {translated}{newline}")
            continue

        output.append(body + newline)

    return "".join(output)


def translate_readme(path: Path, report: Report) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    output: list[str] = []
    in_fence = False
    for line in lines:
        newline = ""
        body = line
        if body.endswith("\n"):
            body, newline = body[:-1], "\n"
        stripped = body.strip()

        # Commands and sample output inside fenced blocks are not prose: leave
        # them exactly as they are.
        if stripped.startswith("```"):
            in_fence = not in_fence
            output.append(body + newline)
            continue
        if in_fence:
            output.append(body + newline)
            continue

        if stripped in LINES:
            output.append(LINES[stripped] + newline)
            report.count()
            continue

        row = README_TABLE_ROW.match(stripped)
        if row:
            objective = row.group(2)
            if objective in OBJECTIVES:
                report.count()
                output.append(
                    f"| `{row.group(1)}` | {OBJECTIVES[objective]} |{newline}"
                )
                continue
            if has_chinese(objective):
                output.append(body + newline)
                continue
            report.add(f"{path}: table row", objective)
            output.append(body + newline)
            continue

        if has_chinese(stripped) or not re.search(r"[A-Za-z]", stripped):
            output.append(body + newline)
            continue

        report.add(f"{path}: markdown line", stripped)
        output.append(body + newline)
    return "".join(output)


def translate_tree(root: Path, report: Report) -> None:
    for directory in ("exercises", "solutions", "templates", "include"):
        base = root / directory
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix in SOURCE_SUFFIXES:
                path.write_text(translate_source(path, report), encoding="utf-8")
            elif path.name == "README.md" and directory == MARKDOWN_DIR:
                path.write_text(translate_readme(path, report), encoding="utf-8")


def rewrite(path: Path, report: Report, strict: bool) -> None:
    translate_tree(path, report)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--list-missing", action="store_true")
    args = parser.parse_args(argv)

    report = Report()
    rewrite(Path(args.root), report, args.strict)

    total_missing = sum(len(items) for items in report.missing.values())
    print(f"translated: {report.translated} lines")
    if total_missing:
        unique: dict[str, int] = {}
        for items in report.missing.values():
            for item in items:
                unique[item] = unique.get(item, 0) + 1
        print(f"missing entries: {total_missing} ({len(unique)} unique)")
        if args.list_missing:
            for text in sorted(unique):
                print(f"  {text}")
        else:
            for text in sorted(unique)[:10]:
                print(f"  {text}")
            if len(unique) > 10:
                print(f"  ... and {len(unique) - 10} more (use --list-missing)")
    if args.strict and total_missing:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
