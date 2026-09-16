#!/usr/bin/env python3
"""Build the beginner distribution zip.

The zip is what a Windows-only learner downloads: the exercises plus, when
``tools/winbox.sh fetch-native`` has been run, a bundled w64devkit compiler and
an embedded Python, so that nothing has to be installed.
"""

from __future__ import annotations

import argparse
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Everything a learner needs; tools/ and the CI files are for maintainers only.
PACKAGE_ITEMS = (
    "clings",
    "clings.cmd",
    "README.md",
    "LICENSE",
    "include",
    "exercises",
    "solutions",
    "templates",
    "docs",
)

RUNTIME_ITEMS = (
    (ROOT / ".winbox" / "native" / "w64devkit", "runtime/mingw"),
    (ROOT / ".winbox" / "native" / "python", "runtime/python"),
)


def upstream_commit() -> str:
    provenance = ROOT / "docs" / "provenance.md"
    if provenance.is_file():
        match = re.search(
            r"^- upstream commit: (\S+)$",
            provenance.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        if match and match.group(1) != "unknown":
            return match.group(1)[:12]
    return "dev"


def build(with_runtime: bool, out_dir: Path) -> Path:
    version = upstream_commit()
    package = f"clings-win-{version}"
    out_dir.mkdir(parents=True, exist_ok=True)
    archive = out_dir / f"{package}.zip"

    with tempfile.TemporaryDirectory(prefix="clings-win-package-") as work:
        stage = Path(work) / package
        stage.mkdir()
        for item in PACKAGE_ITEMS:
            origin = ROOT / item
            if not origin.exists():
                raise SystemExit(f"missing package item: {origin}")
            if origin.is_dir():
                shutil.copytree(
                    origin,
                    stage / item,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
                )
            else:
                shutil.copyfile(origin, stage / item)

        bundled: list[str] = []
        for origin, destination in RUNTIME_ITEMS:
            if origin.is_dir():
                shutil.copytree(origin, stage / destination)
                bundled.append(destination)
            elif with_runtime:
                raise SystemExit(
                    f"{origin} is missing; run 'tools/winbox.sh fetch-native'"
                )

        # Batch files are stored with LF in the repository (see .gitattributes)
        # but cmd.exe is happiest with CRLF, and the zip is what learners get.
        for path in stage.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".cmd", ".bat"}:
                text = path.read_bytes().replace(b"\r\n", b"\n")
                path.write_bytes(text.replace(b"\n", b"\r\n"))

        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
            for path in sorted(stage.rglob("*")):
                if path.is_file():
                    bundle.write(path, path.relative_to(stage.parent))

    print(f"built {archive}")
    print(f"  version: {version}")
    if bundled:
        print(f"  bundled runtime: {', '.join(bundled)}")
    else:
        print("  no bundled toolchain: the user needs Python 3 and gcc on PATH")
    return archive


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir", default=str(ROOT / "dist"), help="where to write the zip"
    )
    parser.add_argument(
        "--with-runtime",
        action="store_true",
        help="fail instead of warning when the bundled runtime is missing",
    )
    args = parser.parse_args(argv)
    build(args.with_runtime, Path(args.out_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
