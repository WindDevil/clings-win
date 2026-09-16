#!/usr/bin/env python3
"""Build the beginner distribution zips.

Two flavours are produced, because the trade-off is real:

* ``-full.zip``  exercises + bundled w64devkit compiler + embedded Python.
  Nothing to install, no PATH changes, no admin rights - but a big download.
* ``-slim.zip``  exercises only.  Small, and the right choice for someone who
  already has a compiler and Python.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
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


def twin_commit() -> str:
    """The commit this package was built from, or "" outside a git checkout."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short=12", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return ""
    return result.stdout.strip()


def package_version() -> str:
    """What goes in the file name.

    The twin commit, not the upstream one: this name has to tell two builds of
    the same exercises apart, and the exercises are only half of what changed
    here.  Naming the zip after upstream meant every rebuild - including the
    one that fixed the console colours - produced the same file name as the
    broken build before it.  Upstream provenance is still recorded in
    docs/provenance.md and in the release notes.
    """
    return twin_commit() or upstream_commit()


def build(with_runtime: bool, out_dir: Path, allow_missing_runtime: bool) -> Path:
    version = package_version()
    flavor = "full" if with_runtime else "slim"
    package = f"clings-win-{version}-{flavor}"
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
            if not with_runtime:
                continue
            if origin.is_dir():
                shutil.copytree(origin, stage / destination)
                bundled.append(destination)
            elif not allow_missing_runtime:
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
    print(f"  version: {version} ({flavor})")
    if bundled:
        print(f"  bundled runtime: {', '.join(bundled)}")
    else:
        print("  no bundled toolchain: the learner needs Python 3 and gcc on PATH")
    return archive


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir", default=str(ROOT / "dist"), help="where to write the zip"
    )
    parser.add_argument(
        "--flavor",
        choices=("slim", "full", "both"),
        default="both",
        help="slim (no toolchain), full (bundled toolchain) or both",
    )
    parser.add_argument(
        "--allow-missing-runtime",
        action="store_true",
        help="still build the full flavour when the bundled runtime is absent",
    )
    args = parser.parse_args(argv)
    out_dir = Path(args.out_dir)
    if args.flavor in ("slim", "both"):
        build(False, out_dir, args.allow_missing_runtime)
    if args.flavor in ("full", "both"):
        build(True, out_dir, args.allow_missing_runtime)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
