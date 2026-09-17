"""The built-in editor's HTTP side.

Standard library only, like the runner: the package ships a Python and a gcc,
and a learner who unzips it should not also need pip.  That rules out a
framework and leaves http.server, which is fine - this serves one page to one
person on one machine.

Three things it is careful about, because a process that writes files on
behalf of a web page ought to be:

* it listens on 127.0.0.1, never 0.0.0.0, and requires a token minted at
  startup, so another process (or another page in the same browser) cannot
  drive it by guessing the port;
* every path a request names goes through ``paths.resolve_within``, so the
  worst a forged request can do is edit an exercise;
* it refuses to run two compiles at once, because the runner's build
  directory and progress file are shared state.

The API is small on purpose.  It is the same five runner calls bridge.py
documents, plus reading and writing the text of an exercise file.
"""

from __future__ import annotations

import hashlib
import json
import mimetypes
import secrets
import sys
import threading
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from . import bridge, paths, vscode
from .languages import all_languages, for_path
from .languages.base import CheckContext

WEB_ROOT = Path(__file__).resolve().parent / "web"
HOST = "127.0.0.1"
DEFAULT_PORT = 8420
# Generous for an exercise, unfriendly to anything using this as a file drop.
MAX_BODY = 1 << 20
TOKEN_HEADER = "X-Clings-Token"


class _State:
    """What the server knows, and the lock that keeps it true.

    ``listing`` and ``toolchain`` each cost a process launch (about 100 ms) and
    change only when the learner does something to the package, so they are
    read once and dropped after anything that could move them.
    """

    def __init__(self) -> None:
        self.token = secrets.token_urlsafe(24)
        self.lock = threading.Lock()
        self.origin = f"http://{HOST}"
        self._listing: bridge.Listing | None = None
        self._toolchain: bridge.Toolchain | None = None

    def listing(self) -> bridge.Listing:
        if self._listing is None:
            self._listing = bridge.listing()
        return self._listing

    def toolchain(self) -> bridge.Toolchain:
        if self._toolchain is None:
            self._toolchain = bridge.toolchain()
        return self._toolchain

    def invalidate(self) -> None:
        self._listing = None
        self._toolchain = None


def _revision(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


class Handler(BaseHTTPRequestHandler):
    server_version = "clings-studio"
    protocol_version = "HTTP/1.1"
    state: _State  # set on the class by serve()

    # -- plumbing ---------------------------------------------------------
    def log_message(self, fmt: str, *args: object) -> None:
        """Keep quiet unless asked: the learner reads a browser, not a console.

        Errors are worth a line - a failed request is the only clue something
        is wrong when the page just stops responding.
        """
        # getattr, not self.server.verbose: serve() is not the only way to
        # build a server, and a missing attribute here would take down the
        # connection rather than print a line.
        if getattr(self.server, "verbose", False):
            sys.stderr.write(f"[studio] {fmt % args}\n")

    def _send(
        self,
        status: HTTPStatus | int,
        body: bytes,
        content_type: str,
        *,
        extra: dict[str, str] | None = None,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        # Nothing here is cacheable: the page and the files both change under
        # the browser, and a stale exercise is worse than a slow one.
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, payload: object, status: HTTPStatus | int = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send(status, body, "application/json; charset=utf-8")

    def _error(self, status: HTTPStatus | int, message: str) -> None:
        self._json({"error": message}, status)

    def _authorised(self, query: dict[str, list[str]]) -> bool:
        """Prove the caller is the page we served, not something that found us.

        Two independent checks, because either alone has a hole: the token
        says "you have read our HTML", and the Origin check says "the browser
        thinks you are our page" - which is what stops a page on some other
        site from posting here with a form.
        """
        origin = self.headers.get("Origin")
        if origin is not None and origin != self.state.origin:
            return False
        given = self.headers.get(TOKEN_HEADER, "")
        if not given:
            given = (query.get("token") or [""])[0]
        return secrets.compare_digest(given, self.state.token)

    def _body(self) -> dict[str, object] | None:
        """The request body as a dict, or None after answering an error."""
        try:
            length = int(self.headers.get("Content-Length") or "0")
        except ValueError:
            self._error(HTTPStatus.BAD_REQUEST, "Content-Length 不合法")
            return None
        if length <= 0:
            return {}
        if length > MAX_BODY:
            self._error(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "请求体太大")
            return None
        raw = self.rfile.read(length)
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            self._error(HTTPStatus.BAD_REQUEST, f"请求体不是 JSON: {error}")
            return None
        if not isinstance(parsed, dict):
            self._error(HTTPStatus.BAD_REQUEST, "请求体必须是 JSON 对象")
            return None
        return parsed

    def _exercise_or_error(self, ident: str) -> bridge.Exercise | None:
        listing = self.state.listing()
        matches = listing.candidates(ident)
        if len(matches) == 1:
            return matches[0]
        if not matches:
            self._error(HTTPStatus.NOT_FOUND, f"找不到这个练习: {ident}")
            return None
        self._json(
            {
                "error": f"练习名有歧义: {ident}",
                "candidates": [item.ident for item in matches],
            },
            HTTPStatus.CONFLICT,
        )
        return None

    # -- routes -----------------------------------------------------------
    def do_GET(self) -> None:  # noqa: N802 - http.server's spelling
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        route = unquote(parsed.path)
        if route == "/":
            return self._index()
        if route.startswith("/static/"):
            return self._static(route[len("/static/") :])
        if route == "/favicon.ico":
            return self._send(HTTPStatus.NO_CONTENT, b"", "image/x-icon")
        if not route.startswith("/api/"):
            return self._error(HTTPStatus.NOT_FOUND, "没有这个地址")
        if not self._authorised(query):
            return self._error(HTTPStatus.FORBIDDEN, "令牌无效，请重新打开编辑器")
        if route == "/api/session":
            return self._session()
        if route == "/api/exercises":
            return self._exercises()
        if route == "/api/file":
            return self._read_file(query)
        if route.startswith("/api/exercise/"):
            return self._exercise(route[len("/api/exercise/") :])
        self._error(HTTPStatus.NOT_FOUND, "没有这个接口")

    def do_HEAD(self) -> None:  # noqa: N802
        self.do_GET()

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        route = unquote(parsed.path)
        if not route.startswith("/api/"):
            return self._error(HTTPStatus.NOT_FOUND, "没有这个地址")
        if not self._authorised(query):
            return self._error(HTTPStatus.FORBIDDEN, "令牌无效，请重新打开编辑器")
        body = self._body()
        if body is None:
            return
        if route == "/api/check":
            return self._check(body)
        if route == "/api/completion":
            return self._completion(body)
        if route == "/api/run":
            return self._run(body)
        if route == "/api/reset":
            return self._mutate(body, "reset")
        if route == "/api/solution":
            return self._mutate(body, "solution")
        if route == "/api/open-vscode":
            return self._open_vscode(body)
        self._error(HTTPStatus.NOT_FOUND, "没有这个接口")

    def do_PUT(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        route = unquote(parsed.path)
        if route != "/api/file":
            return self._error(HTTPStatus.NOT_FOUND, "没有这个地址")
        if not self._authorised(query):
            return self._error(HTTPStatus.FORBIDDEN, "令牌无效，请重新打开编辑器")
        body = self._body()
        if body is None:
            return
        self._write_file(body)

    # -- responses --------------------------------------------------------
    def _index(self) -> None:
        page = WEB_ROOT / "index.html"
        try:
            html = page.read_text(encoding="utf-8")
        except OSError as error:
            return self._error(
                HTTPStatus.INTERNAL_SERVER_ERROR, f"读不到界面文件: {error}"
            )
        # The token rides in the page, so a request the browser did not make
        # from this document cannot be authenticated.  It is a local page that
        # is never cached, so there is nothing for the token to leak into.
        html = html.replace("__CLINGS_TOKEN__", self.state.token)
        self._send(
            HTTPStatus.OK,
            html.encode("utf-8"),
            "text/html; charset=utf-8",
            extra={
                "Content-Security-Policy": (
                    "default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
                    "img-src 'self' data:; connect-src 'self'; font-src 'self'"
                )
            },
        )

    def _static(self, relative: str) -> None:
        try:
            target = paths.resolve_within(WEB_ROOT, relative)
        except paths.PathNotAllowed:
            return self._error(HTTPStatus.FORBIDDEN, "越界路径")
        if not target.is_file():
            return self._error(HTTPStatus.NOT_FOUND, f"没有这个文件: {relative}")
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type in {
            "application/javascript",
            "application/json",
        }:
            content_type += "; charset=utf-8"
        self._send(HTTPStatus.OK, target.read_bytes(), content_type)

    def _session(self) -> None:
        """Everything the page needs once, at load."""
        listing = self.state.listing()
        toolchain = self.state.toolchain()
        editor = vscode.find_editor()
        self._json(
            {
                "root": listing.root,
                "launcher": listing.launcher,
                "total": listing.total,
                "completed_count": listing.completed_count,
                "languages": [item.describe() for item in all_languages()],
                "toolchain": {
                    "compiler": toolchain.compiler,
                    "compiler_found": toolchain.compiler_found,
                    "compiler_version": toolchain.compiler_version,
                    "timeout_seconds": toolchain.timeout_seconds,
                },
                "vscode": {"found": editor is not None, "path": str(editor or "")},
            }
        )

    def _exercises(self) -> None:
        listing = self.state.listing()
        self._json(
            {
                "root": listing.root,
                "launcher": listing.launcher,
                "total": listing.total,
                "completed_count": listing.completed_count,
                "next": (listing.next_exercise().ident if listing.next_exercise() else ""),
                "topics": [
                    {
                        "name": topic.name,
                        "exercises": [
                            {
                                "ident": item.ident,
                                "topic": item.topic,
                                "slug": item.slug,
                                "title": item.title,
                                "objective": item.objective,
                                "is_project": item.is_project,
                                "completed": item.completed,
                                "files": list(item.files),
                            }
                            for item in topic.exercises
                        ],
                    }
                    for topic in listing.topics
                ],
            }
        )

    def _exercise(self, ident: str) -> None:
        exercise = self._exercise_or_error(ident)
        if exercise is None:
            return
        listing = self.state.listing()
        order = listing.exercises
        index = next(
            (position for position, item in enumerate(order) if item.ident == exercise.ident),
            None,
        )
        files = []
        for absolute in paths.exercise_files(exercise):
            language = for_path(absolute)
            files.append(
                {
                    "path": paths.relative(absolute),
                    "name": absolute.name,
                    "editable": paths.is_editable(absolute),
                    "language_id": language.id,
                    "editor_mode": language.editor_mode,
                    "exists": absolute.is_file(),
                }
            )
        self._json(
            {
                "exercise": {
                    "ident": exercise.ident,
                    "topic": exercise.topic,
                    "slug": exercise.slug,
                    "title": exercise.title,
                    "objective": exercise.objective,
                    "hint": exercise.hint,
                    "reference": exercise.reference,
                    "is_project": exercise.is_project,
                    "completed": exercise.completed,
                },
                "files": files,
                # The topic's README is the lesson text, and it belongs to the
                # exercise the way a chapter belongs to a page - but it is
                # generated from upstream, so it comes read-only, alongside the
                # editable files rather than among them.
                "topic_readme": self._topic_readme(exercise),
                "previous": order[index - 1].ident if index not in (None, 0) else "",
                "next": (
                    order[index + 1].ident
                    if index is not None and index + 1 < len(order)
                    else ""
                ),
            }
        )

    @staticmethod
    def _topic_readme(exercise: bridge.Exercise) -> dict[str, object]:
        relative = f"exercises/{exercise.topic}/README.md"
        try:
            target = paths.resolve_within(paths.ROOT, relative)
            text: str | None = target.read_text(encoding="utf-8")
        except (paths.PathNotAllowed, OSError, UnicodeDecodeError):
            text = None
        return {"path": relative, "exists": text is not None, "content": text or ""}

    def _read_file(self, query: dict[str, list[str]]) -> None:
        name = (query.get("path") or [""])[0]
        if not name:
            return self._error(HTTPStatus.BAD_REQUEST, "缺少 path 参数")
        try:
            target = paths.resolve_within(paths.ROOT, name)
        except paths.PathNotAllowed as error:
            return self._error(HTTPStatus.FORBIDDEN, str(error))
        if not self._belongs_to_an_exercise(target):
            return self._error(HTTPStatus.FORBIDDEN, f"{name} 不属于任何练习")
        try:
            text = target.read_text(encoding="utf-8")
        except FileNotFoundError:
            return self._error(HTTPStatus.NOT_FOUND, f"文件不存在: {name}")
        except (OSError, UnicodeDecodeError) as error:
            return self._error(HTTPStatus.INTERNAL_SERVER_ERROR, f"读文件失败: {error}")
        language = for_path(target)
        self._json(
            {
                "path": paths.relative(target),
                "content": text,
                "editable": paths.is_editable(target),
                "language_id": language.id,
                "editor_mode": language.editor_mode,
                "revision": _revision(text),
            }
        )

    def _write_file(self, body: dict[str, object]) -> None:
        name = body.get("path")
        content = body.get("content")
        if not isinstance(name, str) or not isinstance(content, str):
            return self._error(HTTPStatus.BAD_REQUEST, "需要 path 和 content")
        try:
            target = paths.resolve_within(paths.ROOT, name)
        except paths.PathNotAllowed as error:
            return self._error(HTTPStatus.FORBIDDEN, str(error))
        if not self._belongs_to_an_exercise(target):
            return self._error(HTTPStatus.FORBIDDEN, f"{name} 不属于任何练习")
        if not paths.is_editable(target):
            return self._error(HTTPStatus.FORBIDDEN, f"{name} 是只读的")

        # base_revision is the version the client started from.  When it does
        # not match what is on disk, the save would silently undo whatever
        # wrote the file - usually the solution or a reset from another
        # window - so the text goes back to the client instead.
        base = body.get("base_revision")
        if isinstance(base, str) and base:
            try:
                on_disk = _revision(target.read_text(encoding="utf-8"))
            except FileNotFoundError:
                on_disk = ""
            except (OSError, UnicodeDecodeError) as error:
                return self._error(HTTPStatus.INTERNAL_SERVER_ERROR, f"读文件失败: {error}")
            if on_disk and on_disk != base:
                return self._json(
                    {
                        "error": "文件在别处被改过，没有保存",
                        "conflict": True,
                        "path": paths.relative(target),
                        "content": target.read_text(encoding="utf-8"),
                        "revision": on_disk,
                    },
                    HTTPStatus.CONFLICT,
                )
        try:
            target.write_text(content, encoding="utf-8", newline="")
        except OSError as error:
            return self._error(HTTPStatus.INTERNAL_SERVER_ERROR, f"写文件失败: {error}")
        self._json(
            {"ok": True, "path": paths.relative(target), "revision": _revision(content)}
        )

    def _check(self, body: dict[str, object]) -> None:
        name = body.get("path")
        content = body.get("content")
        if not isinstance(name, str) or not isinstance(content, str):
            return self._error(HTTPStatus.BAD_REQUEST, "需要 path 和 content")
        try:
            target = paths.resolve_within(paths.ROOT, name)
        except paths.PathNotAllowed as error:
            return self._error(HTTPStatus.FORBIDDEN, str(error))
        exercise = self._exercise_of(target)
        if exercise is None:
            return self._error(HTTPStatus.FORBIDDEN, f"{name} 不属于任何练习")
        language = for_path(target)
        try:
            context = self._context(exercise, language.id)
        except bridge.RunnerError as error:
            return self._error(HTTPStatus.INTERNAL_SERVER_ERROR, str(error))
        with self.state.lock:
            diagnostics = language.check(target, content, context)
        self._json(
            {
                "path": paths.relative(target),
                "language_id": language.id,
                "diagnostics": [item.as_json() for item in diagnostics],
            }
        )

    def _completion(self, body: dict[str, object]) -> None:
        name = body.get("path")
        content = body.get("content")
        if not isinstance(name, str) or not isinstance(content, str):
            return self._error(HTTPStatus.BAD_REQUEST, "需要 path 和 content")
        try:
            target = paths.resolve_within(paths.ROOT, name)
        except paths.PathNotAllowed as error:
            return self._error(HTTPStatus.FORBIDDEN, str(error))
        exercise = self._exercise_of(target)
        if exercise is None:
            return self._error(HTTPStatus.FORBIDDEN, f"{name} 不属于任何练习")
        language = for_path(target)
        try:
            context = self._context(exercise, language.id)
        except bridge.RunnerError as error:
            return self._error(HTTPStatus.INTERNAL_SERVER_ERROR, str(error))
        items = language.completions(target, content, context)
        self._json(
            {
                "path": paths.relative(target),
                "items": [item.as_json() for item in items],
            }
        )

    def _run(self, body: dict[str, object]) -> None:
        ident = body.get("ident")
        if not isinstance(ident, str) or not ident:
            return self._error(HTTPStatus.BAD_REQUEST, "缺少 ident")
        exercise = self._exercise_or_error(ident)
        if exercise is None:
            return
        stdin_text = body.get("stdin")
        if stdin_text is not None and not isinstance(stdin_text, str):
            return self._error(HTTPStatus.BAD_REQUEST, "stdin 必须是字符串")
        try:
            timeout = self.state.toolchain().timeout_seconds + bridge.RUN_TIMEOUT_MARGIN
        except bridge.RunnerError:
            timeout = bridge.DEFAULT_TIMEOUT
        try:
            # One compile at a time: the runner writes build/ and progress.json,
            # and two runs at once would race for both.
            with self.state.lock:
                result = bridge.run(exercise.ident, stdin_text=stdin_text, timeout=timeout)
                self.state.invalidate()
                listing = self.state.listing()
                context = self._context(exercise, "c")
        except bridge.RunnerError as error:
            return self._error(HTTPStatus.INTERNAL_SERVER_ERROR, str(error))
        diagnostics: list[dict[str, object]] = []
        if not result.passed and result.stage == "compile":
            # A failed build is the editor's business, so hand it over in the
            # same shape as /api/check and the two views cannot disagree.  The
            # text is the file on disk, which is what this run just compiled -
            # the page saves before it runs, so the two are the same text.
            try:
                main = paths.find_file(listing, exercise, exercise.main_file)
                diagnostics = [
                    item.as_json()
                    for item in for_path(main).check(
                        main, main.read_text(encoding="utf-8"), context
                    )
                ]
            except (OSError, UnicodeDecodeError, paths.PathNotAllowed):
                diagnostics = []
        self._json(
            {
                "result": {
                    "ident": result.ident,
                    "title": result.title,
                    "passed": result.passed,
                    "stage": result.stage,
                    "stage_label": result.stage_label,
                    "output": result.output,
                },
                "diagnostics": diagnostics,
                "completed_count": listing.completed_count,
                "total": listing.total,
                "next": (listing.next_exercise().ident if listing.next_exercise() else ""),
            }
        )

    def _mutate(self, body: dict[str, object], action: str) -> None:
        ident = body.get("ident")
        if not isinstance(ident, str) or not ident:
            return self._error(HTTPStatus.BAD_REQUEST, "缺少 ident")
        exercise = self._exercise_or_error(ident)
        if exercise is None:
            return
        with self.state.lock:
            try:
                if action == "reset":
                    output = bridge.reset(exercise.ident)
                elif action == "solution" and body.get("apply"):
                    output = bridge.apply_solution(exercise.ident)
                else:
                    return self._json(
                        {"text": bridge.solution_text(exercise.ident)}, HTTPStatus.OK
                    )
            except bridge.RunnerError as error:
                return self._error(HTTPStatus.INTERNAL_SERVER_ERROR, str(error))
            self.state.invalidate()
            listing = self.state.listing()
        self._json(
            {
                "ok": True,
                "action": action,
                "output": output,
                "completed_count": listing.completed_count,
                "total": listing.total,
            }
        )

    def _open_vscode(self, body: dict[str, object]) -> None:
        ident = body.get("ident")
        if not isinstance(ident, str) or not ident:
            return self._error(HTTPStatus.BAD_REQUEST, "缺少 ident")
        exercise = self._exercise_or_error(ident)
        if exercise is None:
            return
        target = paths.find_file(
            self.state.listing(), exercise, exercise.main_file
        )
        try:
            editor = vscode.open_exercise(target)
        except (FileNotFoundError, ValueError) as error:
            return self._error(HTTPStatus.FAILED_DEPENDENCY, str(error))
        self._json({"ok": True, "editor": str(editor), "path": paths.relative(target)})

    # -- helpers ----------------------------------------------------------
    def _exercise_of(self, target: Path) -> bridge.Exercise | None:
        """The exercise a file belongs to, or None when nothing claims it."""
        for exercise in self.state.listing().exercises:
            if target in paths.exercise_files(exercise):
                return exercise
        return None

    def _belongs_to_an_exercise(self, target: Path) -> bool:
        return self._exercise_of(target) is not None

    def _context(self, exercise: bridge.Exercise, language_id: str) -> CheckContext:
        return CheckContext(
            toolchain=self.state.toolchain(),
            root=paths.ROOT,
            exercise_files=paths.exercise_files(exercise),
            language_id=language_id,
        )


def serve(
    port: int = DEFAULT_PORT,
    *,
    open_browser: bool = True,
    verbose: bool = False,
) -> int:
    """Run the editor until interrupted, and return an exit code."""
    state = _State()
    handler = type("BoundHandler", (Handler,), {"state": state})
    try:
        httpd = ThreadingHTTPServer((HOST, port), handler)
    except OSError as error:
        if port == DEFAULT_PORT:
            # The default port being busy is ordinary - a second window, or
            # something else that picked 8420 - so move rather than fail.
            try:
                httpd = ThreadingHTTPServer((HOST, 0), handler)
            except OSError:
                print(f"无法启动内置编辑器: {error}", file=sys.stderr)
                return 1
        else:
            print(f"端口 {port} 用不了: {error}", file=sys.stderr)
            return 1
    httpd.daemon_threads = True
    httpd.verbose = verbose  # type: ignore[attr-defined]
    state.origin = f"http://{HOST}:{httpd.server_address[1]}"
    url = f"{state.origin}/"
    print(f"内置编辑器: {url}")
    print("按 Ctrl-C 结束。")
    if open_browser:
        threading.Timer(0.3, webbrowser.open, args=(url,)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        httpd.shutdown()
        httpd.server_close()
    return 0
