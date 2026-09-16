#!/usr/bin/env python3
"""Sync the Windows twin from an upstream clings checkout.

The twin never edits exercise content by hand.  This script copies the
upstream learning material, applies the Windows overrides from
tools/windows_overrides.py and rewrites the runner for Windows defaults, so
``--check`` can prove that the twin matches a given upstream commit.

Usage:
    python3 tools/sync_from_source.py --source ../cling
    python3 tools/sync_from_source.py --source ../cling --check
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import windows_overrides as overrides  # noqa: E402
import zh_glossary  # noqa: E402
import zh_translate  # noqa: E402

# Directories and files copied verbatim from upstream, plus the generated
# provenance note.  ``clings`` is copied too and then patched below.
COPY_DIRS = ("include", "exercises", "solutions", "templates")
COPY_FILES = ("clings", "LICENSE")
GENERATED = COPY_DIRS + COPY_FILES + ("docs/provenance.md",)

# Upstream's colour helper assumes the terminal renders ANSI escapes.  Windows
# consoles only do once the process asks for ENABLE_VIRTUAL_TERMINAL_PROCESSING,
# and the first console a learner meets is the one where a stray "\033[36m"
# turns a friendly line into noise.  Swapped wholesale rather than line by
# line; the reasoning is written up in docs/portability.md.
UPSTREAM_COLOR = '''def color(text: str, code: str) -> str:
    if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
        return text
    return f"\\033[{code}m{text}\\033[0m"
'''
WINDOWS_COLOR = '''# Colour is decoration: every message says the same thing with the escapes
# stripped, so a console that cannot render ANSI gets plain text instead.
#
# A Windows console needs *two* output-mode bits before it interprets
# "\\033[36m": ENABLE_VIRTUAL_TERMINAL_PROCESSING and ENABLE_PROCESSED_OUTPUT.
# With only the first one set conhost stores the escape in the screen buffer as
# ordinary characters, which is what turns "运行" into "?[36m运行?[0m" in cmd and
# in Windows PowerShell.  Measured on Windows 10 by writing an escape into a
# console and reading the buffer back: mode 0x4 and 0x6 stay literal, 0x5 and
# 0x7 render the colour.
#
# The mode belongs to the console screen buffer, not to this process: it is
# shared with everything else attached to that window and it outlives clings,
# so switching the bits on is a change the learner's shell inherits.
STD_OUTPUT_HANDLE = -11
ENABLE_PROCESSED_OUTPUT = 0x0001
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
ANSI_CONSOLE_MODE = ENABLE_PROCESSED_OUTPUT | ENABLE_VIRTUAL_TERMINAL_PROCESSING
# The answer cannot change while the process runs, so it is worth one probe.
_ansi_console: bool | None = None


def enable_ansi_console() -> bool:
    """Ask the console behind stdout to render ANSI escapes.

    False means it will not, and colour has to go.  On Windows the console
    needs both output-mode bits above before it interprets an escape, and
    SetConsoleMode refuses a handle that is not a console (a pipe or a file) as
    well as consoles older than Windows 10.  A GetConsoleMode that fails means
    the handle is not a Windows console at all - redirected output, a
    character device such as NUL, or a pipe-backed pseudo terminal - so there
    is no conhost to convince.  (A ConPTY-backed mintty succeeds here with VT
    already on; a Git Bash pty is not even a tty, so color_off_reason has
    already decided before this probe is reached.)
    """
    global _ansi_console
    if _ansi_console is not None:
        return _ansi_console
    if os.name != "nt":
        _ansi_console = True
        return _ansi_console
    try:
        import ctypes

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.GetStdHandle.argtypes = [ctypes.c_uint32]
        kernel32.GetStdHandle.restype = ctypes.c_void_p
        kernel32.GetConsoleMode.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_uint32),
        ]
        kernel32.SetConsoleMode.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        mode = ctypes.c_uint32()
        handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            _ansi_console = True
        elif (mode.value & ANSI_CONSOLE_MODE) == ANSI_CONSOLE_MODE:
            _ansi_console = True
        else:
            wanted = mode.value | ANSI_CONSOLE_MODE
            _ansi_console = bool(kernel32.SetConsoleMode(handle, wanted))
    except (AttributeError, ImportError, OSError, ValueError):
        # A Python whose _ctypes cannot load raises ImportError here; colour is
        # decoration, so it costs plain text and not a traceback.
        _ansi_console = False
    return _ansi_console


def color_off_reason() -> str:
    """Why the output is plain text, or "" when it carries colour.

    CLINGS_COLOR decides first, because it is what a learner reaches for when
    the guess is wrong and what the CI job pins down; then the NO_COLOR
    convention (https://no-color.org/); then auto detection.
    """
    choice = os.environ.get("CLINGS_COLOR", "auto").strip().lower()
    if choice == "never":
        return "CLINGS_COLOR=never"
    if choice != "always":
        if os.environ.get("NO_COLOR"):
            return "NO_COLOR 已设置"
        # A missing stdout (pythonw, or a shell that closed fd 1) is not a
        # terminal either, and asking it would raise instead of answering.
        try:
            interactive = sys.stdout is not None and sys.stdout.isatty()
        except ValueError:
            interactive = False
        if not interactive:
            return "输出不是终端"
        if not enable_ansi_console():
            return "控制台不支持 ANSI"
        return ""
    # Forced on.  A Windows console still has to be asked to render the
    # escapes, or CLINGS_COLOR=always would print them as literal text in the
    # very consoles this whole dance exists to keep readable.
    enable_ansi_console()
    return ""


def color(text: str, code: str) -> str:
    if color_off_reason():
        return text
    return f"\\033[{code}m{text}\\033[0m"
'''

# The runner is copied too, then patched with these exact replacements.  Every
# replacement must match exactly once; otherwise upstream changed the runner
# and this script has to be revisited.
RUNNER_PATCHES: list[tuple[str, str]] = [
    (UPSTREAM_COLOR, WINDOWS_COLOR),
    (
        'DEFAULT_LDLIBS = ["-lm", "-pthread"]\n'
        'if sys.platform.startswith("linux"):\n'
        "    DEFAULT_LDLIBS.append(\"-ldl\")\n",
        'DEFAULT_LDLIBS = ["-lm", "-pthread"]\n'
        "# True on Windows, and on a Linux host running the Wine regression loop\n"
        "# (CLINGS_TARGET=windows) against the mingw-w64 cross compiler.\n"
        'WINDOWS_TARGET = os.name == "nt" or os.environ.get("CLINGS_TARGET") == "windows"\n'
        "if WINDOWS_TARGET:\n"
        "    # Link one self-contained .exe per exercise.  Without this, programs\n"
        "    # that use pthreads need libwinpthread-1.dll next to them, which is\n"
        "    # the classic first blocker for Windows users.\n"
        '    DEFAULT_LDLIBS.append("-static")\n'
        'if sys.platform.startswith("linux") and not WINDOWS_TARGET:\n'
        "    DEFAULT_LDLIBS.append(\"-ldl\")\n",
    ),
    (
        "def compiler() -> str:\n"
        '    return os.environ.get("CC", "cc")\n',
        "def compiler() -> str:\n"
        '    """The C compiler to use, overridable through the CC environment variable."""\n'
        '    default = "gcc" if WINDOWS_TARGET else "cc"\n'
        '    return os.environ.get("CC", default)\n'
        "\n"
        "\n"
        "def exe_suffix() -> str:\n"
        '    """``.exe`` on Windows and for the Wine regression loop."""\n'
        '    return ".exe" if WINDOWS_TARGET else ""\n'
        "\n"
        "\n"
        "def exec_prefix() -> list[str]:\n"
        '    """Launcher placed in front of every built binary.\n'
        "\n"
        "    Empty on Windows.  The Wine regression loop sets CLINGS_EXEC_PREFIX\n"
        "    so PE binaries produced by the cross compiler can be executed.\n"
        '    """\n'
        '    return shlex.split(os.environ.get("CLINGS_EXEC_PREFIX", ""))\n'
        "\n"
        "\n"
        "def launcher() -> str:\n"
        '    """How the learner names this script on the command line.\n'
        "\n"
        "    The two Windows shells agree on exactly one spelling.  cmd.exe reads\n"
        "    a leading './' as a command named '.', and PowerShell does not look\n"
        "    in the current directory at all, so './clings' and a bare 'clings'\n"
        "    each fail in one of them while .\\\\.clings.cmd works in both.\n"
        '    """\n'
        '    return r".\\clings.cmd" if WINDOWS_TARGET else "./clings"\n',
    ),
    (
        '    suffix = "solution" if solution else "exercise"\n'
        '    return BUILD_DIR / exercise.topic / f"{exercise.slug}.{suffix}"\n',
        '    suffix = "solution" if solution else "exercise"\n'
        '    return BUILD_DIR / exercise.topic / f"{exercise.slug}.{suffix}{exe_suffix()}"\n',
    ),
    (
        "    return subprocess.run(\n"
        "        [str(path)],\n"
        "        cwd=ROOT,\n",
        "    return subprocess.run(\n"
        "        [*exec_prefix(), str(path)],\n"
        "        cwd=ROOT,\n",
    ),
    (
        "def main(argv: list[str] | None = None) -> int:\n"
        "    parser = build_parser()\n",
        "def configure_output() -> None:\n"
        '    """Keep Chinese output from crashing a Windows console.\n'
        "\n"
        "    Python takes the console code page (cp936, cp1252, ...) for stdout\n"
        "    and raises UnicodeEncodeError on text it cannot represent.\n"
        "    clings.cmd switches the console to UTF-8; this makes the streams\n"
        "    agree with it, and degrades to '?' instead of a traceback when the\n"
        "    CLI is started some other way.\n"
        '    """\n'
        '    if os.name != "nt":\n'
        "        return\n"
        "    for stream in (sys.stdout, sys.stderr):\n"
        "        try:\n"
        '            stream.reconfigure(encoding="utf-8", errors="replace")\n'
        "        except (AttributeError, ValueError):\n"
        "            pass\n"
        "\n"
        "\n"
        "def main(argv: list[str] | None = None) -> int:\n"
        "    configure_output()\n"
        "    parser = build_parser()\n",
    ),
    (
        "    print(f\"flags:    {' '.join(cflags())}\")\n",
        "    print(f\"flags:    {' '.join(cflags())}\")\n"
        "    # The first thing to check when colour comes out as escape codes:\n"
        "    # which console is this, and did clings decide it can show them?\n"
        "    reason = color_off_reason()\n"
        "    print(f\"颜色:     {'开启' if not reason else '关闭（' + reason + '）'}\")\n",
    ),
]


def normalized_bytes(path: Path) -> bytes:
    """File content with CRLF folded to LF so the twin is host independent."""
    return path.read_bytes().replace(b"\r\n", b"\n")


def patch_runner(text: str) -> str:
    for old, new in RUNNER_PATCHES:
        occurrences = text.count(old)
        if occurrences != 1:
            raise SystemExit(
                "runner patch mismatch: expected 1 occurrence of\n"
                f"---\n{old}---\nfound {occurrences}.\n"
                "Upstream clings changed; update tools/sync_from_source.py."
            )
        text = text.replace(old, new)

    for old, new in zh_glossary.RUNNER:
        if old not in text:
            raise SystemExit(
                "runner translation mismatch, upstream text changed:\n"
                f"---\n{old}---"
            )
        text = text.replace(old, new)
    return text


def git_value(source: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(source), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def provenance(source: Path, tree: Path) -> str:
    exercises = sorted((tree / "exercises").glob("*/*.c"))
    projects = sorted((tree / "exercises").glob("*/*/main.c"))
    topics = {path.parent.name for path in exercises}
    topics |= {path.parent.parent.name for path in projects}
    # Normalized so that a local checkout (…/clings.git) and a CI checkout
    # (…/clings) produce the same file and --check stays meaningful.
    remote = git_value(source, "remote", "get-url", "origin") or str(source)
    remote = remote.removesuffix(".git")
    return (
        "# Provenance\n"
        "\n"
        "Generated by `tools/sync_from_source.py`; do not edit by hand.\n"
        "\n"
        f"- upstream repository: {remote}\n"
        f"- upstream commit: {git_value(source, 'rev-parse', 'HEAD') or 'unknown'}\n"
        f"- topics: {len(topics)}\n"
        f"- exercises: {len(exercises) + len(projects)}\n"
        f"- windows overrides: {len(overrides.rewritten_exercises())}\n"
        "\n"
        "## Windows overrides\n"
        "\n"
        + "".join(f"- `{ident}`\n" for ident in overrides.rewritten_exercises())
    )


def render(source: Path, destination: Path) -> None:
    """Write a complete generated tree into *destination*."""
    for name in COPY_DIRS:
        origin = source / name
        if not origin.is_dir():
            raise SystemExit(f"upstream tree is missing {name}/: {origin}")
        shutil.copytree(
            origin,
            destination / name,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )

    for name in COPY_FILES:
        origin = source / name
        if not origin.is_file():
            raise SystemExit(f"upstream tree is missing {name}: {origin}")
        text = normalized_bytes(origin).decode("utf-8")
        if name == "clings":
            text = patch_runner(text)
        # write_bytes, not write_text: text mode translates every "\n" to
        # os.linesep, so a maintainer running --check on Windows would see the
        # whole tree differ by one byte per line.  The twin is LF everywhere
        # (.gitattributes).  (write_text grew a newline= argument only in 3.10,
        # and these tools run under whatever Python the maintainer has.)
        (destination / name).write_bytes(text.encode("utf-8"))
    (destination / "clings").chmod(0o755)

    overrides.apply(destination)

    docs = destination / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "provenance.md").write_bytes(
        provenance(source, destination).encode("utf-8")
    )

    report = zh_translate.Report()
    zh_translate.translate_tree(destination, report)
    if report.missing:
        unique = sorted({text for items in report.missing.values() for text in items})
        raise SystemExit(
            "English text without a Chinese entry in tools/zh_glossary.py "
            f"({len(unique)} unique):\n"
            + "".join(f"  {text}\n" for text in unique[:20])
            + ("  ...\n" if len(unique) > 20 else "")
            + "add the missing entries, then run sync again"
        )


def compare(generated: Path, current: Path) -> list[str]:
    differences: list[str] = []
    for name in GENERATED:
        left = generated / name
        right = current / name
        if not right.exists():
            differences.append(f"missing: {name}")
            continue
        if left.is_dir():
            comparison = filecmp.dircmp(left, right)
            differences.extend(_walk_differences(comparison, name))
        elif left.read_bytes() != right.read_bytes():
            differences.append(f"differs: {name}")
    return differences


def _walk_differences(comparison: filecmp.dircmp, prefix: str) -> list[str]:
    differences = [f"missing: {prefix}/{name}" for name in comparison.right_only]
    differences += [f"stale: {prefix}/{name}" for name in comparison.left_only]
    differences += [
        f"differs: {prefix}/{name}" for name in comparison.diff_files
    ]
    for name, sub in comparison.subdirs.items():
        differences.extend(_walk_differences(sub, f"{prefix}/{name}"))
    return differences


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        default=str(ROOT.parent / "cling"),
        help="upstream clings checkout (default: sibling ../cling)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail instead of writing when the twin is out of date",
    )
    args = parser.parse_args(argv)

    source = Path(args.source).expanduser().resolve()
    if not (source / "clings").is_file():
        print(f"not an upstream clings checkout: {source}", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="clings-win-sync-") as work:
        generated = Path(work) / "tree"
        generated.mkdir()
        render(source, generated)

        if args.check:
            differences = compare(generated, ROOT)
            if differences:
                print("windows twin is out of date:", file=sys.stderr)
                for entry in differences:
                    print(f"  {entry}", file=sys.stderr)
                print(
                    "run: python3 tools/sync_from_source.py --source "
                    f"{source}",
                    file=sys.stderr,
                )
                return 1
            print("windows twin matches the upstream tree")
            return 0

        for name in COPY_DIRS:
            shutil.rmtree(ROOT / name, ignore_errors=True)
        for name in GENERATED:
            origin = generated / name
            target = ROOT / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if origin.is_dir():
                shutil.rmtree(target, ignore_errors=True)
                shutil.copytree(origin, target)
            else:
                shutil.copyfile(origin, target)
                if name == "clings":
                    target.chmod(0o755)

    report = (ROOT / "docs" / "provenance.md").read_text(encoding="utf-8")
    exercise_line = next(
        line for line in report.splitlines() if line.startswith("- exercises:")
    )
    print(f"synced from {source}")
    print(exercise_line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
