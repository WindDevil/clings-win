"""Everything that is not C yet.

The exercises are C, so this is what a file that no language claims falls back
to: it edits, saves, and says nothing.  That is the point - the alternative is
a syntax checker that is wrong about the text, and a learner who believes it.

Keeping it a real Language rather than a None the callers have to test for is
what makes "not C-only" a property of the design instead of a promise: the
server, the API and the browser go through the same door for both, so the day
someone writes a `python.py` here, nothing else has to change.
"""

from __future__ import annotations

from .base import Language


class PlainLanguage(Language):
    id = "plain"
    label = "纯文本"
    extensions = ()
    editor_mode = "text/plain"
    line_comment = "#"
    block_comment = ("", "")
    tab_size = 4


PLAIN = PlainLanguage()
