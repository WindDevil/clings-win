"""The one place that talks to the clings runner.

The runner is a generated file (``tools/sync_from_source.py`` writes it from
upstream plus the Windows patches), so the studio does not import it, copy its
logic, or read its private state.  It runs it, and reads JSON back:

    clings list --json            exercises, metadata, files, progress
    clings doctor --json          the compiler and the flags a build uses
    clings run <ident> --json     {results: [{passed, stage, output}], ...}
    clings solution <ident>       the reference answer, as source text
    clings reset <ident>          put the original exercise back

Those five calls are the entire contract, and ``tools/sync_from_source.py``
holds the other end of it: a patch that stops matching upstream fails `make
check` rather than silently breaking the studio.  Anything the studio needs
that is not in there belongs in a new ``--json`` field, not in a new parser.

Human-facing output is a separate matter: the menu and the CLI stream the
runner's own text straight to the terminal, colour and all, by running it with
inherited stdio instead of capturing it.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNNER = ROOT / "clings"
# A run is compile + the runner's own timeout; the margin covers a cold
# compiler start on a slow machine, not a slow exercise.
RUN_TIMEOUT_MARGIN = 60.0
DEFAULT_TIMEOUT = 60.0


class RunnerError(RuntimeError):
    """The runner could not be run, or did not answer with the JSON we expect."""


@dataclass(frozen=True)
class Exercise:
    ident: str
    topic: str
    slug: str
    title: str
    objective: str
    reference: str
    hint: str
    is_project: bool
    completed: bool
    files: tuple[str, ...]
    sources: tuple[str, ...]

    @property
    def main_file(self) -> str:
        """The file to put in front of the learner first."""
        return self.files[0] if self.files else ""


@dataclass(frozen=True)
class Topic:
    name: str
    exercises: tuple[Exercise, ...]


@dataclass(frozen=True)
class Listing:
    root: str
    launcher: str
    total: int
    completed_count: int
    topics: tuple[Topic, ...]

    @property
    def exercises(self) -> tuple[Exercise, ...]:
        return tuple(
            exercise for topic in self.topics for exercise in topic.exercises
        )

    def candidates(self, needle: str) -> list[Exercise]:
        """Every exercise the runner would accept this name for.

        Deliberately the same three steps as resolve_exercise() in the runner -
        exact ident, then slug or "/"-suffix, then anything containing the
        text - so that a name the studio accepts is never one the runner would
        reject, and vice versa.
        """
        exercises = self.exercises
        exact = [exercise for exercise in exercises if exercise.ident == needle]
        if exact:
            return exact
        return [
            exercise
            for exercise in exercises
            if exercise.ident.endswith(f"/{needle}")
            or exercise.slug == needle
            or needle in exercise.ident
        ]

    def find(self, needle: str) -> Exercise | None:
        """One exercise by ident, slug, or unambiguous suffix, or None."""
        matches = self.candidates(needle)
        return matches[0] if len(matches) == 1 else None

    def next_exercise(self) -> Exercise | None:
        """The first exercise the learner has not passed, or None."""
        for exercise in self.exercises:
            if not exercise.completed:
                return exercise
        return None


@dataclass(frozen=True)
class Toolchain:
    python: str
    platform: str
    root: str
    launcher: str
    compiler: str
    compiler_found: bool
    compiler_version: str
    cflags: tuple[str, ...]
    ldlibs: tuple[str, ...]
    include_dirs: tuple[str, ...]
    test_source: str
    timeout_seconds: float


@dataclass(frozen=True)
class RunResult:
    ident: str
    title: str
    passed: bool
    stage: str
    output: str

    @property
    def stage_label(self) -> str:
        return {
            "compile": "编译失败",
            "timeout": "运行超时",
            "run": "测试未通过" if not self.passed else "全部通过",
        }.get(self.stage, self.stage)


def _invoke(
    args: list[str],
    *,
    timeout: float | None = DEFAULT_TIMEOUT,
    stdin_text: str | None = None,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run the runner with the interpreter that is running the studio.

    sys.executable, not "python": when the learner starts the studio through
    clings.cmd that is the Python bundled in the package, which is the one the
    exercise toolchain was tested against.  The environment is inherited
    unchanged, so the PATH clings.cmd built (bundled mingw) reaches the
    compiler from here too.
    """
    if not RUNNER.is_file():
        raise RunnerError(f"找不到运行器: {RUNNER}")
    command = [sys.executable, str(RUNNER), *args]
    kwargs: dict[str, object] = {
        "cwd": str(ROOT),
        "text": True,
        # The runner reconfigures its own streams to UTF-8 on Windows, so the
        # bytes on this pipe are UTF-8 no matter what the console code page is.
        "encoding": "utf-8",
        "errors": "replace",
    }
    if capture:
        kwargs["stdout"] = subprocess.PIPE
        kwargs["stderr"] = subprocess.PIPE
    if stdin_text is None:
        # Never inherit the studio's stdin: an exercise that reads input would
        # otherwise block, and under the web server there is nothing to read.
        kwargs["stdin"] = subprocess.DEVNULL
    else:
        kwargs["input"] = stdin_text
    try:
        return subprocess.run(command, timeout=timeout, check=False, **kwargs)  # type: ignore[arg-type]
    except subprocess.TimeoutExpired as error:
        raise RunnerError(f"运行器超时（{timeout:.0f} 秒）: {' '.join(args)}") from error
    except OSError as error:
        raise RunnerError(f"无法启动运行器: {error}") from error


def _invoke_json(
    args: list[str],
    *,
    timeout: float = DEFAULT_TIMEOUT,
    stdin_text: str | None = None,
) -> object:
    result = _invoke(args + ["--json"], timeout=timeout, stdin_text=stdin_text)
    if result.returncode not in (0, 1):
        raise RunnerError(
            f"运行器返回 {result.returncode}: {' '.join(args)}\n{result.stderr.strip()}"
        )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RunnerError(
            f"运行器的输出不是 JSON（{' '.join(args)}）: {error}\n{result.stdout[:400]}"
        ) from error


def _exercise(record: dict[str, object]) -> Exercise:
    def text(key: str) -> str:
        value = record.get(key, "")
        return value if isinstance(value, str) else ""

    def names(key: str) -> tuple[str, ...]:
        value = record.get(key, [])
        return tuple(item for item in value if isinstance(item, str)) if isinstance(value, list) else ()

    return Exercise(
        ident=text("ident"),
        topic=text("topic"),
        slug=text("slug"),
        title=text("title"),
        objective=text("objective"),
        reference=text("reference"),
        hint=text("hint"),
        is_project=bool(record.get("is_project", False)),
        completed=bool(record.get("completed", False)),
        files=names("files"),
        sources=names("sources"),
    )


def listing() -> Listing:
    """Every exercise, with the metadata and progress the editor shows."""
    payload = _invoke_json(["list"])
    if not isinstance(payload, dict):
        raise RunnerError("list --json 没有返回对象")
    topics = []
    for topic in payload.get("topics", []) or []:
        if not isinstance(topic, dict):
            continue
        records = topic.get("exercises", []) or []
        topics.append(
            Topic(
                name=str(topic.get("name", "")),
                exercises=tuple(
                    _exercise(record)
                    for record in records
                    if isinstance(record, dict)
                ),
            )
        )
    return Listing(
        root=str(payload.get("root", ROOT)),
        launcher=str(payload.get("launcher", r".\clings.cmd")),
        total=int(payload.get("total", 0) or 0),
        completed_count=int(payload.get("completed_count", 0) or 0),
        topics=tuple(topics),
    )


def toolchain() -> Toolchain:
    """The compiler and flags the runner builds with.

    The web editor's live diagnostics compile with exactly these, or it would
    report a different set of errors than `run` does for the same file.
    """
    payload = _invoke_json(["doctor"])
    if not isinstance(payload, dict):
        raise RunnerError("doctor --json 没有返回对象")

    def strings(key: str) -> tuple[str, ...]:
        value = payload.get(key, [])
        return tuple(str(item) for item in value) if isinstance(value, list) else ()

    return Toolchain(
        python=str(payload.get("python", "")),
        platform=str(payload.get("platform", "")),
        root=str(payload.get("root", ROOT)),
        launcher=str(payload.get("launcher", r".\clings.cmd")),
        compiler=str(payload.get("compiler", "")),
        compiler_found=bool(payload.get("compiler_found", False)),
        compiler_version=str(payload.get("compiler_version", "")),
        cflags=strings("cflags"),
        ldlibs=strings("ldlibs"),
        include_dirs=strings("include_dirs"),
        test_source=str(payload.get("test_source", "")),
        timeout_seconds=float(payload.get("timeout_seconds", 10.0) or 10.0),
    )


def run(
    ident: str,
    *,
    stdin_text: str | None = None,
    timeout: float | None = None,
) -> RunResult:
    """Compile and run one exercise, and report what happened.

    ``stage`` is the runner's own "compile" / "run" / "timeout", so a caller
    can label a failure without pattern matching the output text.
    """
    if timeout is None:
        try:
            timeout = toolchain().timeout_seconds + RUN_TIMEOUT_MARGIN
        except RunnerError:
            timeout = DEFAULT_TIMEOUT
    payload = _invoke_json(["run", ident], timeout=timeout, stdin_text=stdin_text)
    if not isinstance(payload, dict):
        raise RunnerError("run --json 没有返回对象")
    results = payload.get("results", []) or []
    first = results[0] if results and isinstance(results[0], dict) else {}
    return RunResult(
        ident=str(first.get("ident", ident)),
        title=str(first.get("title", "")),
        passed=bool(first.get("passed", False)),
        stage=str(first.get("stage", "run")),
        output=str(first.get("output", "")),
    )


def run_streaming(ident: str | None = None) -> int:
    """Run one exercise with the terminal attached, exactly as `clings run`.

    Used by the double-click path: an exercise that reads stdin has to be able
    to read the keyboard, and the learner should see the runner's colours.
    """
    args = ["run"] if ident is None else ["run", ident]
    # No deadline of our own: the learner is at the keyboard, the runner
    # already bounds the exercise itself, and Ctrl-C reaches the child because
    # the terminal is shared.
    result = _invoke(args, capture=False, timeout=None)
    return result.returncode


def solution_text(ident: str) -> str:
    """The reference answer for one exercise, as it would be printed."""
    result = _invoke(["solution", ident])
    if result.returncode != 0:
        raise RunnerError(result.stdout.strip() or result.stderr.strip() or "读不到参考答案")
    return result.stdout


def apply_solution(ident: str) -> str:
    """Write the reference answer over the learner's file(s)."""
    result = _invoke(["solution", ident, "--apply"])
    if result.returncode != 0:
        raise RunnerError(result.stdout.strip() or result.stderr.strip() or "应用参考答案失败")
    return result.stdout.strip()


def reset(ident: str) -> str:
    """Put the original exercise back and clear its progress."""
    result = _invoke(["reset", ident])
    if result.returncode != 0:
        raise RunnerError(result.stdout.strip() or result.stderr.strip() or "重置失败")
    return result.stdout.strip()
