"""What every module here needs and none of them should grow its own copy of.

No test cases live in this file; a name that does not start with "test" is
invisible to discovery, which is the point.

Two jobs:

* a web server on a port nobody else is using, so the HTTP tests can talk to
  the real handler without a fixed port and without colliding with a studio
  the learner happens to have open; and
* putting the tree back exactly as it was found.  Several tests have to let
  the runner write to exercises/ - that is what "run" does - so restoring is
  part of the test, not an afterthought for when it fails.
"""

from __future__ import annotations

import contextlib
import http.client
import json
import threading
import unittest
from collections import namedtuple
from http.server import ThreadingHTTPServer
from pathlib import Path

from .. import bridge, paths, server
from ..languages import CheckContext

ROOT = Path(__file__).resolve().parent.parent.parent
# Where the runner records passes; gitignored, but a learner's real progress
# all the same, so tests that can move it put it back.
PROGRESS = ROOT / ".clings" / "progress.json"

Response = namedtuple("Response", "status payload headers")

_TOOLCHAIN: bridge.Toolchain | None = None


def toolchain() -> bridge.Toolchain:
    """The toolchain, read once: each read is a runner launch."""
    global _TOOLCHAIN
    if _TOOLCHAIN is None:
        _TOOLCHAIN = bridge.toolchain()
    return _TOOLCHAIN


def compiler_ready() -> bool:
    """Whether there is a compiler to test the C side against.

    A RunnerError is deliberately not caught here: no compiler is an ordinary
    machine and worth skipping on, but a checkout where `clings doctor` cannot
    answer at all is broken, and a skip would hide that.
    """
    return toolchain().compiler_found


LISTING: bridge.Listing | None = None


def listing() -> bridge.Listing:
    """The exercise list, read once: 185 exercises, one runner launch."""
    global LISTING
    if LISTING is None:
        LISTING = bridge.listing()
    return LISTING


def exercise(ident: str) -> bridge.Exercise:
    found = listing().find(ident)
    if found is None:  # pragma: no cover - the tests name known exercises
        raise AssertionError(f"测试用到的练习不存在: {ident}")
    return found


def files_of(ident: str) -> tuple[Path, ...]:
    return paths.exercise_files(exercise(ident))


def check_context(ident: str, language_id: str = "c") -> CheckContext:
    """A CheckContext for one exercise, the way the server builds it."""
    return CheckContext(
        toolchain=toolchain(),
        root=ROOT,
        exercise_files=files_of(ident),
        language_id=language_id,
    )


@contextlib.contextmanager
def unchanged(*targets: Path):
    """Put these files back byte for byte, whether the test passed or not.

    Byte for byte, not "the text": the generated tree is LF, .cmd files are
    CRLF, and a rewrite that normalises either one would show up as a diff in
    a tree that is supposed to be generated.  A file the test created and the
    tree did not have is removed: a learner's progress.json appearing where
    there was none before is still a change.
    """
    saved = {path: path.read_bytes() for path in targets if path.is_file()}
    try:
        yield
    finally:
        for path in targets:
            if path in saved:
                if not path.is_file() or path.read_bytes() != saved[path]:
                    path.write_bytes(saved[path])
            elif path.is_file():
                path.unlink()


_SOLUTIONS: dict[str, str] = {}


def solution(ident: str) -> str:
    """One reading of a reference answer per run: each is a runner launch.

    The solution is the fixture of choice for anything that needs C that
    compiles: CI verifies every one of them, whatever the learner has done to
    the exercises themselves.
    """
    if ident not in _SOLUTIONS:
        _SOLUTIONS[ident] = bridge.solution_text(ident)
    return _SOLUTIONS[ident]


# Two ways to be wrong that do not depend on the text being appended to: an
# exercise's own code varies, but a missing semicolon is a missing semicolon.
NO_SEMICOLON = "\nint clings_probe_unsolved(void) { return 1 }\n"
IMPLICIT = "\nint clings_probe_unsolved(void) { return clings_probe_missing(); }\n"


class Server:
    """A studio server on an ephemeral port, alive for one test case.

    The same construction serve() uses, minus serve_forever(): the point is to
    exercise the real handler, so nothing here is stubbed except the port.
    """

    def __init__(self) -> None:
        self.state = server._State()
        handler = type("BoundHandler", (server.Handler,), {"state": self.state})
        self.httpd = ThreadingHTTPServer((server.HOST, 0), handler)
        self.httpd.daemon_threads = True
        self.port = self.httpd.server_address[1]
        self.state.origin = f"http://{server.HOST}:{self.port}"
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    @property
    def token(self) -> str:
        return self.state.token

    def close(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=10)

    def request(
        self,
        method: str,
        route: str,
        body: object = None,
        *,
        token: bool = True,
        origin: str | None = None,
        raw: bytes | None = None,
        timeout: float = 180.0,
    ) -> Response:
        """One request.  ``raw`` sends bytes as they are, for the bad ones."""
        payload = raw
        if payload is None and body is not None:
            payload = json.dumps(body).encode("utf-8")
        headers = {}
        if payload is not None:
            headers["Content-Type"] = "application/json"
            headers["Content-Length"] = str(len(payload))
        if token:
            headers[server.TOKEN_HEADER] = self.state.token
        if origin is not None:
            headers["Origin"] = origin
        connection = http.client.HTTPConnection(server.HOST, self.port, timeout=timeout)
        try:
            connection.request(method, route, body=payload, headers=headers)
            response = connection.getresponse()
            data = response.read()
            content_type = response.getheader("Content-Type", "")
            payload_value: object
            if "json" in content_type:
                payload_value = json.loads(data.decode("utf-8"))
            else:
                payload_value = data.decode("utf-8", "replace")
            return Response(response.status, payload_value, dict(response.getheaders()))
        finally:
            connection.close()


class ServerCase(unittest.TestCase):
    """A TestCase with a server, minus the setUp/tearDown boilerplate."""

    server: Server

    def setUp(self) -> None:
        self.server = Server()
        self.addCleanup(self.server.close)
