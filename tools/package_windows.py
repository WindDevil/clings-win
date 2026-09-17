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
import os
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
    # The editor a learner gets without VS Code.  Delete this line and the
    # package still compiles, runs and checks every exercise; only the
    # no-editor case goes away - clings.cmd detects the missing directory.
    "studio",
    # Not an editor, but what makes the VS Code one work: the C/C++ extension
    # only sees include/ if a workspace config says so.
    ".vscode",
)

RUNTIME_ITEMS = (
    (ROOT / ".winbox" / "native" / "w64devkit", "runtime/mingw"),
    (ROOT / ".winbox" / "native" / "python", "runtime/python"),
)

EMBEDDED_PYTHON_MARKER = (
    "# clings: the package root, so `python -m studio` (the double-click menu\n"
    "# and `web`) can import it even though a ._pth file switches PYTHONPATH off.\n"
)

IGNORED = ("__pycache__", "*.pyc")
# The studio's tests ship nowhere.  They are maintainer material, they need a
# checkout to be meaningful, and running them rewrites exercises - which is
# exactly what a learner's copy should never do behind their back.
IGNORED_IN_STUDIO = (*IGNORED, "tests")


def patch_embedded_python(python_dir: Path, package_root: Path) -> list[Path]:
    """Make the bundled embeddable Python able to import the studio.

    The embeddable distribution ships a ``python3xx._pth`` file, and CPython
    reads that file as *the* contents of ``sys.path``: it turns on isolated
    mode, switches ``PYTHONPATH`` and ``PYTHONHOME`` off, and keeps the
    current directory (and the script's) out of the search path.  So the
    ``PYTHONPATH`` that clings.cmd sets is exactly the variable the bundled
    interpreter ignores, and ``python -m studio`` dies with "No module named
    studio" in the full package while working fine in the slim one, where the
    learner's own Python honours it.

    Adding the package root to the ``._pth`` file is the supported way to say
    it: the entries in that file are read relative to the directory the file
    itself sits in, so ``..\\..`` means "the root of the unpacked package"
    whatever folder the learner unzipped it into.

    Returns the files that were changed (empty when there is no ``._pth``
    file, in which case the interpreter honours ``PYTHONPATH`` as usual).
    """
    if not python_dir.is_dir():
        return []
    # Learned from the layout rather than hard-coded, so moving runtime/python
    # under another level cannot leave a ._pth entry pointing at the wrong
    # directory.
    entry = os.path.relpath(package_root, python_dir).replace("/", "\\")
    changed: list[Path] = []
    for path in sorted(python_dir.glob("*._pth")):
        data = path.read_bytes()
        lines = [
            line.partition("#")[0].strip()
            for line in data.decode("utf-8").splitlines()
        ]
        if any(line.replace("/", "\\") == entry for line in lines):
            continue
        if not data.endswith(b"\n"):
            data += b"\n"
        # Written as bytes: the file belongs to Windows, and the zips are
        # built on Linux too.
        path.write_bytes(data + (EMBEDDED_PYTHON_MARKER + entry + "\n").encode("utf-8"))
        changed.append(path)
    return changed


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
                    ignore=shutil.ignore_patterns(
                        *(IGNORED_IN_STUDIO if item == "studio" else IGNORED)
                    ),
                )
            else:
                shutil.copyfile(origin, stage / item)

        bundled: list[str] = []
        patched: list[str] = []
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

        if with_runtime and (stage / "runtime" / "python").is_dir():
            patched = [
                path.relative_to(stage).as_posix()
                for path in patch_embedded_python(
                    stage / "runtime" / "python", stage
                )
            ]

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
    for path in patched:
        # The embeddable Python ignores PYTHONPATH; this is the line that
        # makes `python -m studio` work in the package shipping it.
        print(f"  added the package root to {path}")
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
