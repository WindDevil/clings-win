"""The languages the editor can open, and how a file picks one.

A registry, and nothing else: the callers ask ``for_path()`` or
``all_languages()`` and never import a language module by name.  Adding one is
writing the module and adding a line to ``LANGUAGES``.
"""

from __future__ import annotations

from pathlib import Path

from .base import CheckContext, Completion, Diagnostic, Language
from .c import CLanguage
from .plain import PLAIN

LANGUAGES: tuple[Language, ...] = (CLanguage(),)
# What a file with no owner gets.  Not None: see plain.py.
FALLBACK = PLAIN

__all__ = [
    "CheckContext",
    "Completion",
    "Diagnostic",
    "Language",
    "LANGUAGES",
    "FALLBACK",
    "all_languages",
    "by_id",
    "for_path",
]


def for_path(path: Path | str) -> Language:
    """The language that should open *path*.

    The longest matching extension wins.  That only comes up when one
    extension is a suffix of another - a file called "notes.tar.gz" ends in
    both ".gz" and ".tar.gz" - and the longer, more specific one is what the
    caller meant.  Registering the fallback's extensions is not needed: a file
    nobody claims gets FALLBACK.
    """
    name = str(path).lower()
    best: Language | None = None
    best_length = -1
    for language in LANGUAGES:
        for extension in language.extensions:
            if name.endswith(extension.lower()) and len(extension) > best_length:
                best, best_length = language, len(extension)
    return best or FALLBACK


def by_id(language_id: str) -> Language | None:
    for language in LANGUAGES:
        if language.id == language_id:
            return language
    return FALLBACK if language_id == FALLBACK.id else None


def all_languages() -> tuple[Language, ...]:
    """Every language, fallback included, for the browser to be told about."""
    return (*LANGUAGES, FALLBACK)
