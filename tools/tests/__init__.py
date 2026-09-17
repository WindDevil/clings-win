"""Tests for the packaging and generation steps.

    python -m unittest discover -s tools/tests -t .

These are the maintainer-side scripts: the ones whose bugs reach a learner as
a broken download rather than as a failing exercise.  They need no Windows, no
Wine and no compiler - the parts that do are covered by the workflows in
.github/ and by docs/windows-smoke-test.md.
"""
