"""`python -m studio ...`, which is what clings.cmd calls for these verbs.

    python -m studio open [练习]     open an exercise in VS Code
    python -m studio web [选项]      start the built-in editor
    python -m studio menu [练习]     run an exercise, then stay open

Nothing here is on the path of an ordinary `clings.cmd run`: the launcher only
reaches this module for `open`, `web`, and the no-argument case, so a learner
who never wants the studio never loads it.
"""

from __future__ import annotations

import argparse
import sys

from . import menu, server, vscode

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m studio",
        description="clings 的编辑器：用 VS Code 打开，用内置网页编辑器打开，"
                    "或者跑一遍再问你要做什么。",
        epilog="不带命令时等于 menu。",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="{open,web,menu}")
    open_parser = subparsers.add_parser("open", help="用 VS Code 打开一个练习")
    open_parser.add_argument("exercise", nargs="?", help="练习名，例如 01_printf")
    web_parser = subparsers.add_parser("web", help="启动内置编辑器")
    web_parser.add_argument(
        "--port", type=int, default=server.DEFAULT_PORT,
        help=f"端口，默认 {server.DEFAULT_PORT}，被占用时自动换一个",
    )
    web_parser.add_argument(
        "--no-browser", action="store_true", help="不自动打开浏览器，只打印地址",
    )
    menu_parser = subparsers.add_parser("menu", help="运行练习后显示菜单")
    menu_parser.add_argument("exercise", nargs="?", help="练习名，例如 01_printf")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    # No command at all is the double-click case; say so rather than printing
    # argparse's help at someone who did not ask a question.
    if not args:
        return menu.run(None)
    parser = build_parser()
    try:
        parsed = parser.parse_args(args)
    except SystemExit as exit_code:
        # argparse prints its own message; pass the code through.  --help
        # arrives here too, with 0.
        return int(exit_code.code or 0)

    if parsed.command == "open":
        return vscode.main([parsed.exercise] if parsed.exercise else [])
    if parsed.command == "web":
        return server.serve(parsed.port, open_browser=not parsed.no_browser)
    if parsed.command == "menu":
        return menu.run(parsed.exercise)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
