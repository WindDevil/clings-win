"""What a language has to provide, and nothing about which one it is.

Everything the editor knows about C lives in ``c.py``; the server, the API and
the browser only ever see the shapes below.  That is the whole reason this
module exists: adding a language should mean adding a file here, not touching
the editor.

A language answers two questions:

* what is wrong with this text (``check``) - the server compiles with it, so
  the answer is the same one `run` will give, not an approximation; and
* what could the learner type next (``completions``) - which is the language's
  vocabulary plus whatever the exercise itself defines.

Both are optional: ``plain.py`` answers neither, and is still a perfectly good
language for editing a file nobody claims.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass
from pathlib import Path

from ..bridge import Toolchain


@dataclass(frozen=True)
class Diagnostic:
    """One thing the compiler said about one place in the text."""

    line: int
    column: int
    severity: str  # "error" | "warning" | "note" | "info"
    message: str
    file: str = ""  # package-relative; "" means the file being edited
    code: str = ""  # the -W flag, when the compiler named one
    context: str = ""  # the source line and caret the compiler echoed back

    def as_json(self) -> dict[str, object]:
        return {
            "line": self.line,
            "column": self.column,
            "severity": self.severity,
            "message": self.message,
            "file": self.file,
            "code": self.code,
            "context": self.context,
        }


@dataclass(frozen=True)
class Completion:
    """One thing the learner could type at the cursor."""

    label: str
    kind: str  # "keyword" | "type" | "function" | "macro" | "snippet"
    detail: str = ""
    insert: str = ""
    header: str = ""  # where it comes from, e.g. <stdio.h> or "本练习"

    def as_json(self) -> dict[str, object]:
        return {
            "label": self.label,
            "kind": self.kind,
            "detail": self.detail,
            "insert": self.insert or self.label,
            "header": self.header,
        }


@dataclass(frozen=True)
class CheckContext:
    """What a language needs to know about *this* package to check a file."""

    toolchain: Toolchain
    root: Path
    # The other files of the exercise, by absolute path.  A header is checked
    # together with the .c files that include it - on its own it would not
    # compile, and reporting that would be a lie.
    exercise_files: tuple[Path, ...] = ()
    language_id: str = ""


class Language(abc.ABC):
    """One language the editor can open."""

    id: str = ""
    label: str = ""
    extensions: tuple[str, ...] = ()
    # Presentation only: how CodeMirror should colour this text.  The client
    # maps these to a mode; it is not expected to know the language.
    editor_mode: str = "text/plain"
    line_comment: str = "//"
    block_comment: tuple[str, str] = ("/*", "*/")
    tab_size: int = 4
    # Whether the two optional methods below do anything.  The browser uses
    # these to decide what to offer: asking a language that cannot answer would
    # cost a round trip to be told nothing, and worse, would let the editor
    # imply it had checked something it had not.
    checks: bool = False
    completes: bool = False

    def check(self, path: Path, content: str, context: CheckContext) -> list[Diagnostic]:
        """Report what is wrong with *content*, or [] when nothing is known."""
        return []

    def completions(
        self, path: Path, content: str, context: CheckContext
    ) -> list[Completion]:
        """Report what could follow the cursor, or [] when nothing is known."""
        return []

    def describe(self) -> dict[str, object]:
        """The part of a language the browser needs, for /api/session."""
        return {
            "id": self.id,
            "label": self.label,
            "extensions": list(self.extensions),
            "editor_mode": self.editor_mode,
            "line_comment": self.line_comment,
            "block_comment": list(self.block_comment),
            "tab_size": self.tab_size,
            "checks": self.checks,
            "completes": self.completes,
        }
