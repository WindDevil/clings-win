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

# Machine-readable output.  Everything the twin adds on top of the exercises -
# the studio in studio/, and whatever reaches it through a shell - talks to the
# runner through this and nothing else: no imports, no parsing of the human
# output, no second copy of "where do exercises live and what is in them".
# ``--json`` is deliberately generic (a listing, a toolchain report, a run
# result) so that the interface stays the runner's, not the studio's.
JSON_LIST_BLOCK = r'''def exercise_files(exercise: Exercise) -> list[Path]:
    """Every file that belongs to an exercise, in the order to show them.

    For the five multi-file exercises this is the whole directory: the .c
    files that get compiled, and the headers they include, which are just as
    much the learner's to edit but never appear on a command line.
    """
    files = list(exercise.sources)
    if exercise.is_project:
        files.extend(sorted(exercise.path.parent.glob("*.h")))
    return files


def exercise_record(exercise: Exercise, completed: set[str]) -> dict[str, object]:
    """The machine-readable shape of one exercise.

    A consumer that only has this JSON must be able to render the exercise
    list on its own, so it carries the header metadata, whether the learner
    has passed it, the files that make it up, and which of them a build
    actually compiles.  Paths are relative to ROOT with forward slashes,
    which reads the same on a POSIX host and on Windows.
    """
    return {
        "ident": exercise.ident,
        "topic": exercise.topic,
        "slug": exercise.slug,
        "title": exercise.title,
        "objective": exercise.objective,
        "reference": exercise.reference,
        "hint": exercise.hint,
        "is_project": exercise.is_project,
        "completed": exercise.ident in completed,
        "files": [
            path.relative_to(ROOT).as_posix() for path in exercise_files(exercise)
        ],
        "sources": [
            source.relative_to(ROOT).as_posix() for source in exercise.sources
        ],
    }


def emit_json(payload: object) -> None:
    """Write one JSON document and flush it.

    ensure_ascii=False keeps the Chinese titles readable to a human reading
    the raw output; consumers decode UTF-8, which configure_output already
    guarantees for this process on Windows.
    """
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    sys.stdout.flush()


def command_list(args: argparse.Namespace) -> int:
    exercises = discover()
    completed = load_progress()
    if not exercises:
        print(red("no exercises found"))
        return 1

    if getattr(args, "json", False):
        topics: list[dict[str, object]] = []
        for exercise in exercises:
            if args.topic and exercise.topic != args.topic:
                continue
            if not topics or topics[-1]["name"] != exercise.topic:
                topics.append({"name": exercise.topic, "exercises": []})
            listed = topics[-1]["exercises"]
            if isinstance(listed, list):
                listed.append(exercise_record(exercise, completed))
        emit_json(
            {
                "root": str(ROOT),
                "launcher": launcher(),
                "total": len(exercises),
                "completed_count": sum(
                    1 for exercise in exercises if exercise.ident in completed
                ),
                "topics": topics,
            }
        )
        return 0

    current_topic = None
'''

JSON_RUN_BLOCK = r'''    json_mode = bool(getattr(args, "json", False))
    completed = load_progress()
    failures = 0
    results: list[dict[str, object]] = []
    for exercise in targets:
        if not json_mode:
            print(f"\n{cyan('running')} {exercise.ident} - {exercise.title}")
        passed, output, stage = run_exercise(exercise, verbose=args.verbose)
        results.append(
            {
                "ident": exercise.ident,
                "title": exercise.title,
                "passed": passed,
                "stage": stage,
                "output": output,
            }
        )
        if passed:
            completed.add(exercise.ident)
            save_progress(completed)
            if not json_mode:
                print(green("  passed"))
            if args.verbose and output and not json_mode:
                print(output, end="" if output.endswith("\n") else "\n")
            continue

        failures += 1
        if not json_mode:
            print(red("  failed"))
            if output:
                print(output, end="" if output.endswith("\n") else "\n")
        if not args.continue_on_error:
            break

    if json_mode:
        emit_json(
            {
                "results": results,
                "failures": failures,
                "completed_count": sum(
                    1 for exercise in exercises if exercise.ident in completed
                ),
            }
        )
        return 1 if failures else 0
    if failures:
        print(red(f"\n{failures} exercise(s) failed"))
        return 1
    print(green("\nall selected exercises passed"))
    return 0
'''

JSON_DOCTOR_BLOCK = r'''    if getattr(args, "json", False):
        import inspect

        # A missing compiler is a state the caller has to be able to report -
        # the slim package expects the learner to have installed one - so it
        # must not come back as a traceback.
        try:
            probe = subprocess.run(
                [compiler(), "--version"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            version = probe.stdout.splitlines()[0] if probe.stdout else ""
        except OSError:
            version = ""
        emit_json(
            {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "root": str(ROOT),
                "launcher": launcher(),
                "compiler": compiler(),
                "compiler_found": bool(version),
                "compiler_version": version,
                # A caller that shows diagnostics while the learner types has
                # to compile the way `run` does, or it reports a different set
                # of errors than the exercise itself does.  These are the only
                # flags and search paths that decide that.
                "cflags": cflags(),
                "ldlibs": DEFAULT_LDLIBS,
                "include_dirs": [
                    (ROOT / "include").relative_to(ROOT).as_posix(),
                    ".",
                ],
                "test_source": "include/clings/test.c",
                # Read off run_binary rather than repeated here, so a caller
                # that puts its own deadline around a run cannot drift away
                # from the deadline the runner itself applies.
                "timeout_seconds": inspect.signature(run_binary)
                .parameters["timeout"]
                .default,
            }
        )
        return 0
'''

# What a beginner gets after a failed run.  The exercises are *designed* to
# fail before they are edited - `clings selftest` enforces exactly that - so
# the first thing a learner sees from `run` is a compiler error or a failed
# test, and a compiler error on its own reads like "my installation is broken"
# rather than "this is the exercise".  The runner prints it rather than
# clings.cmd or the studio, so that every way into `run` - a double-click, the
# menu, a typed command - says the same thing.
NEXT_STEPS_BLOCK = r'''

def next_steps(exercise: Exercise) -> None:
    """Name the file and the two commands that move a stuck learner forward.

    The blank in the exercise is the teaching device and the compiler output
    is what it teaches with.  This adds the sentence neither of them can: that
    the failure is the starting point, and which file to open.
    """
    print()
    print("  这道题一开始就是通不过的：文件里留了空（注释里的 TODO），报错就是它给的线索。")
    print(f"  要改的文件:  {exercise.path.relative_to(ROOT)}")
    print(f"  看提示:      {launcher()} hint {exercise.ident}")
    print(f"  改完重跑:    {launcher()} run {exercise.ident}")
'''

# A missing compiler is the one failure a beginner can hit before the first
# exercise even starts: the slim package asks them to install MinGW-w64, and
# installing it "nearly right" (not on PATH) is the classic first wall.  Left
# alone, subprocess raises FileNotFoundError and the learner gets a Python
# traceback that says nothing about what to install.  The compiler call is
# wrapped instead, and main() prints this.
MISSING_COMPILER_BLOCK = r'''class ToolchainError(RuntimeError):
    """The C compiler this package compiles with is not there at all."""


def missing_compiler_message() -> str:
    return (
        red(f"没有找到 C 编译器: {compiler()}") + "\n"
        "  这个包自带的编译器在 runtime\\mingw\\bin（只有 -full.zip 才有）；\n"
        "  它不在的话，重新解压一份 full 包，或者自己装 MinGW-w64 并把 gcc 放进 PATH。\n"
        f"  看当前工具链: {launcher()} doctor\n"
        "  装好之后，把刚才那条命令再跑一遍。"
    )


def compile_sources(
    sources: tuple[Path, ...],
    output: Path,
    include_dirs: tuple[Path, ...] = (),
) -> subprocess.CompletedProcess[str]:
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        compiler(),
        *cflags(),
        f"-I{ROOT / 'include'}",
    ]
    for directory in include_dirs:
        command.append(f"-I{directory}")
    command.extend(str(source) for source in sources)
    command.append(str(ROOT / "include" / "clings" / "test.c"))
    command.extend(["-o", str(output), *DEFAULT_LDLIBS])
    try:
        return subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    except OSError as error:
        raise ToolchainError(missing_compiler_message()) from error
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
    # --- machine-readable output, for the studio and for scripts ------------
    (
        r'''def command_list(args: argparse.Namespace) -> int:
    exercises = discover()
    completed = load_progress()
    if not exercises:
        print(red("no exercises found"))
        return 1

    current_topic = None
''',
        JSON_LIST_BLOCK,
    ),
    (
        r'''def run_exercise(exercise: Exercise, verbose: bool = False) -> tuple[bool, str]:
    output = binary_path(exercise)
    include_dirs = (exercise.path.parent,) if exercise.is_project else ()
    build = compile_sources(exercise.sources, output, include_dirs)
    if build.returncode != 0:
        return False, "compilation failed\n" + build.stdout

    try:
        result = run_binary(output)
    except subprocess.TimeoutExpired:
        return False, "exercise timed out after 10 seconds"

    if verbose or result.returncode != 0:
        return result.returncode == 0, result.stdout
    return result.returncode == 0, result.stdout
''',
        r'''def run_exercise(
    exercise: Exercise, verbose: bool = False
) -> tuple[bool, str, str]:
    """Compile and run one exercise.

    The third element names the stage that produced this result - "compile",
    "run" or "timeout" - so a caller reporting it to a learner can say which
    one failed without matching on the message text.
    """
    output = binary_path(exercise)
    include_dirs = (exercise.path.parent,) if exercise.is_project else ()
    build = compile_sources(exercise.sources, output, include_dirs)
    if build.returncode != 0:
        return False, "compilation failed\n" + build.stdout, "compile"

    try:
        result = run_binary(output)
    except subprocess.TimeoutExpired:
        return False, "exercise timed out after 10 seconds", "timeout"

    if verbose or result.returncode != 0:
        return result.returncode == 0, result.stdout, "run"
    return result.returncode == 0, result.stdout, "run"
''',
    ),
    (
        r'''    completed = load_progress()
    failures = 0
    for exercise in targets:
        print(f"\n{cyan('running')} {exercise.ident} - {exercise.title}")
        passed, output = run_exercise(exercise, verbose=args.verbose)
        if passed:
            completed.add(exercise.ident)
            save_progress(completed)
            print(green("  passed"))
            if args.verbose and output:
                print(output, end="" if output.endswith("\n") else "\n")
            continue

        failures += 1
        print(red("  failed"))
        if output:
            print(output, end="" if output.endswith("\n") else "\n")
        if not args.continue_on_error:
            break

    if failures:
        print(red(f"\n{failures} exercise(s) failed"))
        return 1
    print(green("\nall selected exercises passed"))
    return 0
''',
        JSON_RUN_BLOCK,
    ),
    (
        '            passed, output = run_exercise(exercise, verbose=True)\n',
        '            passed, output, _ = run_exercise(exercise, verbose=True)\n',
    ),
    (
        "        passed, _ = run_exercise(exercise)\n",
        "        passed, _, _ = run_exercise(exercise)\n",
    ),
    (
        'def command_doctor(args: argparse.Namespace) -> int:\n'
        '    print(f"python:   {platform.python_version()}")\n',
        'def command_doctor(args: argparse.Namespace) -> int:\n'
        + JSON_DOCTOR_BLOCK
        + '    print(f"python:   {platform.python_version()}")\n',
    ),
    (
        '    list_parser.add_argument("--topic", help="only show one topic")\n',
        '    list_parser.add_argument("--topic", help="only show one topic")\n'
        '    list_parser.add_argument("--json", action="store_true", help="以 JSON 输出")\n',
    ),
    (
        '    run_parser.add_argument("--verbose", action="store_true")\n',
        '    run_parser.add_argument("--verbose", action="store_true")\n'
        '    run_parser.add_argument("--json", action="store_true", help="以 JSON 输出")\n',
    ),
    (
        '    doctor_parser = subparsers.add_parser("doctor", help="show toolchain information")\n',
        '    doctor_parser = subparsers.add_parser("doctor", help="show toolchain information")\n'
        '    doctor_parser.add_argument("--json", action="store_true", help="以 JSON 输出")\n',
    ),
    # --- a failed run explains itself, for the learner ----------------------
    # Anchored on upstream's command_hint rather than on command_run: that one
    # is rewritten by JSON_RUN_BLOCK above, so the placement stays stable
    # however the JSON blocks change.  Applied last, after those blocks, so
    # that the call site below matches the text they wrote.
    (
        "def command_hint(args: argparse.Namespace) -> int:\n",
        NEXT_STEPS_BLOCK.lstrip("\n") + "\n\ndef command_hint(args: argparse.Namespace) -> int:\n",
    ),
    (
        '        failures += 1\n'
        '        if not json_mode:\n'
        '            print(red("  failed"))\n'
        '            if output:\n'
        '                print(output, end="" if output.endswith("\\n") else "\\n")\n',
        '        failures += 1\n'
        '        if not json_mode:\n'
        '            print(red("  failed"))\n'
        '            if output:\n'
        '                print(output, end="" if output.endswith("\\n") else "\\n")\n'
        '            next_steps(exercise)\n',
    ),
    # --- a missing compiler is a toolchain message, not a traceback --------
    (
        r'''def compile_sources(
    sources: tuple[Path, ...],
    output: Path,
    include_dirs: tuple[Path, ...] = (),
) -> subprocess.CompletedProcess[str]:
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        compiler(),
        *cflags(),
        f"-I{ROOT / 'include'}",
    ]
    for directory in include_dirs:
        command.append(f"-I{directory}")
    command.extend(str(source) for source in sources)
    command.append(str(ROOT / "include" / "clings" / "test.c"))
    command.extend(["-o", str(output), *DEFAULT_LDLIBS])
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
''',
        MISSING_COMPILER_BLOCK,
    ),
    (
        "    try:\n"
        "        return int(args.func(args))\n"
        "    except KeyboardInterrupt:\n",
        "    try:\n"
        "        return int(args.func(args))\n"
        "    except ToolchainError as error:\n"
        "        print(error)\n"
        "        return 2\n"
        "    except KeyboardInterrupt:\n",
    ),
    # --- a name that does not resolve is not a finished course --------------
    # resolve_exercise() answers None both for "no name given and nothing left
    # to do" and for "that name is unknown or ambiguous".  Only the first one
    # is worth a green line and an exit code of 0; the second already printed
    # why, and telling a learner "all exercises are complete" after a typo -
    # then reporting success to whatever called clings - is wrong twice.
    (
        "def command_next(args: argparse.Namespace) -> int:\n"
        "    exercise = resolve_exercise(args.exercise)\n"
        "    if exercise is None:\n"
        '        print(green("All exercises are complete. Try `./clings verify`."))\n'
        "        return 0\n",
        "def command_next(args: argparse.Namespace) -> int:\n"
        "    exercise = resolve_exercise(args.exercise)\n"
        "    if exercise is None:\n"
        "        if args.exercise:\n"
        "            return 1\n"
        '        print(green("All exercises are complete. Try `./clings verify`."))\n'
        "        return 0\n",
    ),
    (
        "    if args.all:\n"
        "        targets = exercises\n"
        "    else:\n"
        "        exercise = resolve_exercise(args.exercise)\n"
        "        if exercise is None:\n"
        '            print(green("All exercises are complete. Try `./clings verify`."))\n'
        "            return 0\n"
        "        targets = [exercise]\n",
        "    if args.all:\n"
        "        targets = exercises\n"
        "    else:\n"
        "        exercise = resolve_exercise(args.exercise)\n"
        "        if exercise is None:\n"
        "            if args.exercise:\n"
        "                return 1\n"
        '            print(green("All exercises are complete. Try `./clings verify`."))\n'
        "            return 0\n"
        "        targets = [exercise]\n",
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
