"""What a double-click on clings.cmd does: run the exercise, then stay open.

A window that opens, prints a list and closes is the behaviour this replaces.
The shape is: run the current exercise with the terminal attached (so a
program that reads the keyboard still works, and the learner sees the runner's
own colours), then offer the four things they are most likely to want next.

The learner here is a first-year student who has never used a terminal, so the
window also has to say what "it" is: the first run orients them (see _welcome),
every run names the file to edit, and the menu names that file next to "用 VS
Code 打开" - which is useless without it.

Everything here goes through the runner or through bridge.py.  Nothing in this
file knows how an exercise is compiled - when the flags change upstream, this
keeps working, which is the point of the split.
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import bridge, paths, server, vscode

CHOICES = (
    ("1", "改完了，重跑一遍"),
    ("2", "用 VS Code 打开"),
    ("3", "打开内置编辑器（浏览器）"),
    ("4", "看这道题的提示"),
    ("0", "退出"),
)


def _display(relative: str) -> str:
    """A package-relative path spelled the way the learner's own shell does."""
    return str(Path(relative))


def choices(exercise: bridge.Exercise | None = None) -> tuple[tuple[str, str], ...]:
    """The menu, naming the file wherever the learner has to open one.

    "[2] 用 VS Code 打开" only helps if the *what* is spelled out, and the
    learner may never have seen the tree this package is.
    """
    if exercise is None:
        return CHOICES
    named = _display(exercise.main_file)
    return tuple(
        (key, f"{label} {named}" if key == "2" else label)
        for key, label in CHOICES
    )


def _rule(title: str = "") -> None:
    if title:
        print(f"\n── {title} " + "─" * max(0, 46 - len(title)))
    else:
        print()
    # The exercise runs with this process's stdout handed to it, and Python
    # block-buffers a redirected stdout: without this flush the header arrives
    # after the compiler output whenever the output is not a terminal.
    sys.stdout.flush()


def _show(exercise: bridge.Exercise) -> None:
    _rule(f"{exercise.ident}  {exercise.title}")
    if exercise.objective:
        print(f"  {exercise.objective}")
    print(f"  要改的文件: {_display(exercise.main_file)}")
    if exercise.is_project:
        print("  （这道题有多个文件，都是你要改的）")
    # This block is what the learner reads *before* the compiler output, and
    # the run below hands the terminal to a child process - a redirected
    # stdout would otherwise flush these lines after it.
    sys.stdout.flush()


def _welcome(listing: bridge.Listing) -> None:
    """The orientation a first-year student needs and nothing else gives them.

    Printed on every double-click until the first exercise is passed, rather
    than exactly once: a learner who is stuck on exercise one is precisely the
    one who closes the window and comes back tomorrow, and re-reading this
    costs them less than having to remember where they were.
    """
    _rule("第一次用，先看这里")
    print(f"  这个包里有 {listing.total} 道 C 语言练习题，每道题都是一个能编译、"
          "能运行的程序，")
    print("  里面留了一处空（注释里写着 TODO）。打开文件、把空补上、保存，再跑一遍就会通过。")
    print()
    print("  一开始不通过是正常的：报错就是这道题给你的线索，不是环境装坏了。")
    print("  做过的题会记下来，下次双击 clings.cmd 接着做没做完的那一道。")
    print()
    print("  改文件有三种办法，挑一种就行：")
    print(r"    记事本      在 exercises\ 里找到练习文件，右键 →「打开方式」→ 记事本")
    print("    VS Code     跑完在下面的菜单里按 2")
    print("    内置编辑器   在下面的菜单里按 3，用浏览器写，有高亮和自动查错")
    _rule()


def _hint(exercise: bridge.Exercise) -> None:
    _rule("提示")
    print(f"  {exercise.hint or '这个练习没有提示。'}")


def _open_editor(exercise: bridge.Exercise) -> None:
    """Hand the browser the built-in editor, and wait for it.

    Blocking is deliberate: the server owns a port and a terminal, and it
    would be rude to leave it running behind a menu the learner thinks they
    have left.
    """
    _rule("内置编辑器")
    print("  浏览器里编辑，Ctrl-S 保存，Ctrl-Enter 运行。")
    print(f"  想直接编辑 {exercise.ident}，在左边列表里选它。")
    server.serve(open_browser=True)
    _rule("编辑器已关闭")


def _open_vscode(exercise: bridge.Exercise, listing: bridge.Listing) -> None:
    _rule("VS Code")
    try:
        target = paths.find_file(listing, exercise, exercise.main_file)
        editor = vscode.open_exercise(target)
    except FileNotFoundError as error:
        print(error)
        return
    except (paths.PathNotAllowed, ValueError) as error:
        print(f"  打不开: {error}")
        return
    print(f"  已用 {editor} 打开：{target}")


def _next_hint(exercise: bridge.Exercise) -> None:
    """Say what comes next, when the exercise just passed.

    Printed rather than added to the menu: the menu is about *this* exercise,
    and a learner who has just got something working should be told the one
    command that moves on, not offered a fifth thing to choose between.
    """
    listing = bridge.listing()
    order = listing.exercises
    for index, item in enumerate(order):
        if item.ident != exercise.ident or index + 1 >= len(order):
            return
        following = order[index + 1]
        print(f"\n  下一个练习：{following.title}")
        print(f"    {listing.launcher} run {following.ident}")
        return


def choose(exercise: bridge.Exercise | None = None) -> str:
    """One menu answer, or "0" for anything that means stop."""
    print()
    for key, label in choices(exercise):
        print(f"  [{key}] {label}")
    try:
        answer = input("选择: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return "0"
    return answer


def run(ident: str | None = None) -> int:
    """Run an exercise, then stay for the menu.  Returns a process exit code."""
    try:
        listing = bridge.listing()
    except bridge.RunnerError as error:
        print(f"读不到练习列表: {error}", file=sys.stderr)
        return 1

    exercise = listing.find(ident) if ident else listing.next_exercise()
    if exercise is None:
        if ident:
            matches = listing.candidates(ident)
            if matches:
                print(f"练习名有歧义: {ident}", file=sys.stderr)
                for item in matches:
                    print(f"  {item.ident}", file=sys.stderr)
            else:
                print(f"找不到这个练习: {ident}", file=sys.stderr)
        else:
            print("所有练习都完成了。想重做的话，从下面的菜单里选“打开内置编辑器”。")
        return 1

    if not listing.completed_count:
        _welcome(listing)
    _show(exercise)
    code = bridge.run_streaming(exercise.ident)
    # The exit code says the harness ran; progress says the exercise passed,
    # and those differ for a run that fails its checks.
    try:
        passed = _passed(exercise.ident)
    except bridge.RunnerError:
        passed = code == 0
    if passed:
        _next_hint(exercise)

    while True:
        answer = choose(exercise)
        if answer in ("0", "q", "quit", "exit", ""):
            return 0
        if answer == "1":
            _show(exercise)
            bridge.run_streaming(exercise.ident)
        elif answer == "2":
            _open_vscode(exercise, listing)
        elif answer == "3":
            _open_editor(exercise)
        elif answer == "4":
            _hint(exercise)
        else:
            print("  请输入 1、2、3、4 或 0。")


def _passed(ident: str) -> bool:
    """Whether the runner recorded a pass, read back from progress."""
    for exercise in bridge.listing().exercises:
        if exercise.ident == ident:
            return exercise.completed
    return False
