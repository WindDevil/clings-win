"""clings studio: the optional desktop helpers around the clings runner.

Two things live here, and both of them are *additions* to the package rather
than part of it:

* opening an exercise in the editor the learner already has (VS Code), and
* a built-in web editor for the learner who has none.

The rule that keeps this from growing into a second copy of clings: nothing
in here imports the runner.  `clings` is a generated file whose internals are
not a contract, so the studio treats it as a command line - see
``studio/bridge.py`` for the whole of that interface.  Delete this directory
and `clings.cmd` still runs every exercise; ``clings.cmd`` only routes the
``open`` / ``web`` / no-argument verbs here.
"""

__all__ = ["bridge", "languages", "menu", "server", "vscode"]
