"""Tests for the studio: the parts of it that are not a browser.

They run against the real runner and a real compiler, because the thing worth
testing here is a contract with a generated file - a stub would only ever
prove that the stub agrees with itself.  What needs to hold:

    python -m unittest discover -s studio/tests -t .

Anything that needs a compiler is skipped, not failed, when there is none:
`clings doctor` is the thing that tells a learner about a missing toolchain,
and these tests have no business saying it twice.
"""
