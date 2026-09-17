"""Find the learner's editor, and open an exercise in it.

VS Code is the one to look for because it is what a beginner on Windows is
most likely to have, but the point of this module is smaller than that: turn
"open this exercise" into one command, and when there is nothing to open it
with, say so in a way that leads somewhere (`clings.cmd web`).

Nothing here is on the critical path.  If VS Code is missing, or installed
somewhere this module has never heard of, `open` reports it and the learner
still has the built-in editor and the command line.
"""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

# Creators of the "open in the same window" family.  The CLI shipped with VS
# Code (`bin/code.cmd` on Windows) takes both; `--goto` is how a caller says
# "and put the cursor on this line".
GOTO = "--goto"
REUSE = "--reuse-window"

WINDOWS_CLI_NAMES = ("code.cmd", "code.exe", "code")
UNIX_CLI_NAMES = ("code", "code-insiders", "codium")
# The binary the CLI is a wrapper around.  Opening it directly avoids cmd.exe
# and the argument quoting that comes with it, so it is the preferred route
# when it exists.
WINDOWS_GUI = "Code.exe"

# Where the installers put it when the learner did not tick "add to PATH".
# The user-scope installer is the default download, so it comes first.
INSTALL_DIRS = (
    r"%LOCALAPPDATA%\Programs\Microsoft VS Code",
    r"%LOCALAPPDATA%\Programs\Microsoft VS Code Insiders",
    r"%ProgramFiles%\Microsoft VS Code",
    r"%ProgramFiles(x86)%\Microsoft VS Code",
    r"%ProgramW6432%\Microsoft VS Code",
)
# A portable install (unzipped anywhere) leaves no trace but the uninstall
# key the user created by hand, if anything; the registry search below covers
# the ordinary installs, this covers a directory someone told us about.
ENV_OVERRIDES = ("CLINGS_VSCODE", "CLINGS_EDITOR")


def _expand(value: str) -> Path | None:
    expanded = os.path.expandvars(value)
    if "%" in expanded:
        return None
    if expanded.startswith("~"):
        expanded = str(Path.home()) + expanded[1:]
    return Path(expanded)


def _from_env(name: str) -> Path | None:
    """An explicit choice, which wins over every guess below it."""
    value = os.environ.get(name)
    if not value:
        return None
    # Allow "code --wait"-style values the way VISUAL/EDITOR traditionally do.
    parts = shlex.split(value, posix=False)
    if not parts:
        return None
    candidate = Path(parts[0].strip('"'))
    return candidate if candidate.exists() else None


def _from_path() -> Path | None:
    names = WINDOWS_CLI_NAMES if os.name == "nt" else UNIX_CLI_NAMES
    for name in names:
        found = shutil.which(name)
        if found:
            return Path(found)
    return None


def _from_install_dirs() -> Path | None:
    for template in INSTALL_DIRS:
        directory = _expand(template)
        if directory is None or not directory.is_dir():
            continue
        for relative in (rf"bin\{WINDOWS_CLI_NAMES[0]}", WINDOWS_GUI, "bin/code"):
            candidate = directory / relative
            if candidate.is_file():
                return candidate
    return None


def _from_registry() -> Path | None:
    """Read the uninstall entries the installers write.

    Both the user and the machine installer record InstallLocation there, and
    the display name is the only stable handle: the key itself is "Microsoft
    VS Code" for the user installer and a GUID for the machine one.
    """
    if os.name != "nt":
        return None
    try:
        import winreg
    except ImportError:  # pragma: no cover - not Windows
        return None

    roots = (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE)
    uninstall = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
    for root in roots:
        try:
            with winreg.OpenKey(root, uninstall) as key:
                subkeys = [
                    winreg.EnumKey(key, index)
                    for index in range(winreg.QueryInfoKey(key)[0])
                ]
        except OSError:
            continue
        for subkey in subkeys:
            try:
                with winreg.OpenKey(root, f"{uninstall}\\{subkey}") as entry:
                    name = str(winreg.QueryValueEx(entry, "DisplayName")[0])
                    if "Visual Studio Code" not in name:
                        continue
                    location = str(winreg.QueryValueEx(entry, "InstallLocation")[0])
            except OSError:
                continue
            for relative in (rf"bin\{WINDOWS_CLI_NAMES[0]}", WINDOWS_GUI):
                candidate = Path(location) / relative
                if candidate.is_file():
                    return candidate
    return None


def find_editor() -> Path | None:
    """The best available way to open a file in VS Code, or None."""
    for name in ENV_OVERRIDES:
        found = _from_env(name)
        if found:
            return found
    for probe in (_from_path, _from_install_dirs, _from_registry):
        found = probe()
        if found:
            return found
    return None


def editor_name(editor: Path) -> str:
    return "VS Code"


def install_hint() -> str:
    return (
        "没有找到 VS Code。\n"
        "  安装：https://code.visualstudio.com/Download（安装时勾选"
        "“添加到 PATH”最省事）\n"
        "  或者用内置编辑器：.\\clings.cmd web\n"
        "  已经装在别处的话，设置环境变量 CLINGS_VSCODE 指向 code.cmd"
    )


def plan(targets: list[Path], *, line: int | None = None) -> list[str]:
    """The exact command line that would open *targets*.

    Separate from running it so that the arguments can be looked at - in a
    test, or in a bug report - without a window appearing on someone's desk.
    """
    editor = find_editor()
    if editor is None:
        raise FileNotFoundError(install_hint())
    if not targets:
        raise ValueError("open_files() 需要至少一个路径")
    # One window: a learner double-clicking clings.cmd twice should not end up
    # with two copies of the same folder.  --goto carries the cursor and applies
    # to the file that follows it, so it goes last and names one file - a
    # folder may precede it, which is how you get the workspace *and* the
    # cursor in the same window.
    if line is not None:
        return [
            str(editor),
            REUSE,
            *[str(target) for target in targets[:-1]],
            GOTO,
            f"{targets[-1]}:{line}",
        ]
    return [str(editor), REUSE, *[str(target) for target in targets]]


def open_files(targets: list[Path], *, line: int | None = None) -> Path:
    """Open paths in VS Code and return the editor that was used.

    Raises FileNotFoundError when there is no editor to open them with, so the
    caller decides what to tell the learner.
    """
    args = plan(targets, line=line)
    _spawn(args)
    return Path(args[0])


def _spawn(args: list[str]) -> None:
    """Start the editor without waiting, and without a console flash.

    The CLI is a .cmd on Windows, which means cmd.exe runs it: that is a
    console window the learner did not ask for.  CREATE_NO_WINDOW keeps it
    hidden.  The editor keeps running after this process exits.
    """
    flags = 0
    if os.name == "nt":
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        if Path(args[0]).suffix.lower() in {".cmd", ".bat"}:
            args = ["cmd", "/c", *args]
    try:
        subprocess.Popen(
            args,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=flags,
            close_fds=True,
        )
    except OSError as error:
        raise FileNotFoundError(f"无法启动编辑器: {error}") from error


def open_exercise(path: Path, line: int | None = None) -> Path:
    """Open one exercise file, with the repository open as the folder.

    The folder matters: .vscode/c_cpp_properties.json in the package root is
    what tells the C/C++ extension where include/ is, and that only applies
    when the workspace is the folder.  The file is opened with --goto so the
    cursor lands where the compiler complained.
    """
    root = Path(__file__).resolve().parent.parent
    if line is None:
        return open_files([root, path])
    # The folder comes first even when a line is asked for: without it, a VS
    # Code start that has no window yet would open a single file with no
    # workspace, and the include/ configuration above would not apply.
    return open_files([root, path], line=line)


def main(argv: list[str] | None = None) -> int:
    """`python -m studio open` - open an exercise without the web editor."""
    from . import bridge, paths

    args = list(sys.argv[1:] if argv is None else argv)
    listing = bridge.listing()
    needle = args[0] if args else None
    exercise = listing.find(needle) if needle else listing.next_exercise()
    if exercise is None:
        if needle:
            print(f"找不到这个练习: {needle}", file=sys.stderr)
        else:
            print("所有练习都完成了。", file=sys.stderr)
        return 1
    target = paths.find_file(listing, exercise, exercise.main_file)
    try:
        open_exercise(target)
    except FileNotFoundError as error:
        print(error, file=sys.stderr)
        return 1
    print(f"已在 VS Code 中打开 {exercise.ident}：{target}")
    return 0
