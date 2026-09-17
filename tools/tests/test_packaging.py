"""The packaging step, tested where it does not need Windows.

One line of tools/package_windows.py decides whether the beginner download
works at all, and it is easy to lose without noticing: the full package ships
the *embeddable* Python, whose ``python3xx._pth`` file replaces ``sys.path``
outright.  ``PYTHONPATH`` is ignored there, so ``python -m studio`` - the
double-click menu and ``web`` - dies with "No module named studio" while every
exercise keeps compiling and running, because the runner is a single script
that only needs the standard library.

That is exactly what shipped in v0.3.0.  These tests hold the packaging step
to writing the package root into the ``._pth`` file, at whatever depth the
runtime directory happens to sit.
"""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from tools import package_windows

# Trimmed to the lines that matter; the real file also has 35 binary members
# next to it in the zip.
EMBEDDED_PTH = (
    "python312.zip\n"
    ".\n"
    "\n"
    "# Uncomment to run site.main() automatically\n"
    "#import site\n"
)


class WritingTheEmbeddedPath(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.python = self.root / "runtime" / "python"
        self.python.mkdir(parents=True)
        self.pth = self.python / "python312._pth"
        self.pth.write_text(EMBEDDED_PTH, encoding="utf-8")

    def entries(self, path: Path | None = None) -> list[str]:
        text = (path or self.pth).read_text(encoding="utf-8")
        return [line.partition("#")[0].strip() for line in text.splitlines()]

    def roots(self, pth_dir: Path, path: Path | None = None) -> set[Path]:
        """Where the entries point, read the way CPython reads them.

        The ._pth file is a Windows artifact, so the entries are Windows
        paths even when the zip is built on Linux - and Path() on Linux will
        not split on a backslash.
        """
        return {
            (pth_dir / entry.replace("\\", "/")).resolve()
            for entry in self.entries(path)
            if entry
        }

    def test_the_package_root_ends_up_on_sys_path(self) -> None:
        changed = package_windows.patch_embedded_python(self.python, self.root)
        self.assertEqual([path.name for path in changed], ["python312._pth"])
        self.assertIn(self.root.resolve(), self.roots(self.python))

    def test_the_interpreters_own_lines_survive(self) -> None:
        package_windows.patch_embedded_python(self.python, self.root)
        self.assertIn("python312.zip", self.entries())
        self.assertIn(".", self.entries())
        # site is commented out in the embeddable zip on purpose; un-commenting
        # it would change what the interpreter loads at startup.
        self.assertNotIn("import site", self.entries())

    def test_patching_twice_changes_nothing(self) -> None:
        package_windows.patch_embedded_python(self.python, self.root)
        once = self.pth.read_bytes()
        self.assertEqual(package_windows.patch_embedded_python(self.python, self.root), [])
        self.assertEqual(self.pth.read_bytes(), once)

    def test_the_entry_follows_the_layout(self) -> None:
        # A runtime one level deeper must get one more "..", not a copy of the
        # spelling that happens to be right today.
        deep = self.python / "3.12"
        deep.mkdir()
        (deep / "python312._pth").write_text(EMBEDDED_PTH, encoding="utf-8")
        package_windows.patch_embedded_python(deep, self.root)
        self.assertIn(
            self.root.resolve(),
            self.roots(deep, deep / "python312._pth"),
        )

    def test_another_python_version_is_patched_too(self) -> None:
        other = self.python / "python313._pth"
        other.write_text(EMBEDDED_PTH, encoding="utf-8")
        changed = package_windows.patch_embedded_python(self.python, self.root)
        self.assertEqual(sorted(path.name for path in changed), ["python312._pth", "python313._pth"])

    def test_a_python_without_a_pth_file_is_left_alone(self) -> None:
        empty = self.root / "elsewhere"
        empty.mkdir()
        self.assertEqual(package_windows.patch_embedded_python(empty, self.root), [])
        self.assertEqual(package_windows.patch_embedded_python(self.root / "gone", self.root), [])


class TheFullPackage(unittest.TestCase):
    """build() with a runtime: what actually lands in the learner's zip."""

    def test_the_zip_carries_the_patched_path_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp) / "python"
            runtime.mkdir()
            (runtime / "python312._pth").write_text(EMBEDDED_PTH, encoding="utf-8")
            (runtime / "python.exe").write_bytes(b"MZ")
            out = Path(tmp) / "dist"
            with mock.patch.object(
                package_windows, "RUNTIME_ITEMS", ((runtime, "runtime/python"),)
            ), contextlib.redirect_stdout(io.StringIO()) as printed:
                archive = package_windows.build(True, out, allow_missing_runtime=False)

            self.assertIn("added the package root", printed.getvalue())
            with zipfile.ZipFile(archive) as bundle:
                names = bundle.namelist()
                pth = next(name for name in names if name.endswith("._pth"))
                root = pth.split("/runtime/python/")[0]
                entries = [
                    line.partition("#")[0].strip()
                    for line in bundle.read(pth).decode("utf-8").splitlines()
                ]
                # The interpreter's own entries, then the root of the package
                # in the spelling Windows uses.
                self.assertIn("python312.zip", entries)
                self.assertEqual(entries[-1], "..\\..")
                # ...and what the ._pth file points at is really in the zip:
                # the double-click entry point, and the studio it has to
                # import for the menu and for `web`.
                self.assertIn(f"{root}/clings.cmd", names)
                self.assertIn(f"{root}/studio/__main__.py", names)
                # cmd.exe wants CRLF, and the zip is what a learner gets.
                self.assertIn(b"\r\n", bundle.read(f"{root}/clings.cmd"))
                # The studio's own tests are maintainer material.
                self.assertFalse([name for name in names if "/studio/tests/" in name])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
