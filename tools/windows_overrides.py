"""Windows variants for the few clings exercises that are not portable as written.

This module is the only hand-written difference between the upstream clings
tree and the Windows twin.  Everything else is copied verbatim by
tools/sync_from_source.py, so the two projects cannot drift apart.

Two kinds of overrides exist:

* ``SUBSTITUTIONS`` - line level rewrites applied to the solution, the initial
  exercise and the template.  Use this when only a compiler/CRT detail differs
  and the exercise itself stays the same.
* ``WHOLE_FILE`` - complete replacement files, per role, when the platform API
  is structurally different (dlopen -> LoadLibrary, fork -> _spawnv).

Every substitution is applied exactly once and a mismatch is a hard error, so
an upstream change to one of these files is reported instead of silently
producing a broken Windows tree.
"""

from __future__ import annotations

from pathlib import Path

# Applied to solutions/<rel>.c, exercises/<rel>.c and templates/<rel>.c.
SUBSTITUTIONS: dict[str, list[tuple[str, str]]] = {
    "03_types_variables/01_integer_types": [
        (
            "    CLINGS_CHECK_INT(long_can_hold_int((long)INT_MAX), 1);\n"
            "    CLINGS_CHECK_INT(long_can_hold_int((long)INT_MAX + 1L), 0);\n",
            "    CLINGS_CHECK_INT(long_can_hold_int((long)INT_MAX), 1);\n"
            "    {\n"
            "        /* Data models differ between platforms: LP64 (Linux) keeps\n"
            "         * INT_MAX in a long, LLP64 (Windows) does not.  Compiling\n"
            "         * \"INT_MAX + 1\" as a long is therefore only valid when long\n"
            "         * is genuinely wider than int. */\n"
            "        long above_int_max = (long)INT_MAX;\n"
            "        if (sizeof(long) > sizeof(int)) {\n"
            "            CLINGS_CHECK_INT(long_can_hold_int(above_int_max + 1), 0);\n"
            "        } else {\n"
            "            CLINGS_CHECK_MSG(sizeof(long) == sizeof(int),\n"
            "                             \"long is not wider than int here\");\n"
            "        }\n"
            "    }\n",
        ),
    ],
    "12_standard_library/11_environment": [
        (
            " * objective: Read and write environment variables with getenv and setenv.\n",
            " * objective: Read and write environment variables with getenv and _putenv_s.\n",
        ),
        (
            " * hint: setenv must succeed before getenv can find the new value.\n",
            " * hint: _putenv_s must succeed before getenv can find the new value.\n",
        ),
        (
            "    if (setenv(name, value, 1) != 0) {\n",
            "    if (_putenv_s(name, value) != 0) {\n",
        ),
        (
            "    unsetenv(name);\n",
            "    _putenv_s(name, \"\");\n",
        ),
    ],
    "13_character_io/02_eof_ferror": [
        (
            "    CLINGS_CHECK_INT(feof(file), 1);\n",
            "    /* feof() only promises a non-zero result.  The Microsoft CRT\n"
            "     * returns its internal flag (0x10) instead of 1. */\n"
            "    CLINGS_CHECK_MSG(feof(file) != 0, \"feof() reports end-of-file\");\n",
        ),
    ],
}

_DYNAMIC_LINKING_SOLUTION = r'''
/*
 * clings exercise: 17_translation_units/05_dynamic_linking
 * title: Dynamic linking with LoadLibrary
 * objective: Load a symbol from a shared library at runtime.
 * hint: Use LoadLibraryA, GetProcAddress and FreeLibrary; convert FARPROC through a union.
 */

#include "clings/test.h"

#include <stddef.h>
#include <windows.h>

typedef size_t (*strlen_function)(const char *);

int dynamic_strlen(void)
{
    HMODULE handle = LoadLibraryA("msvcrt.dll");
    if (handle == NULL) {
        return -1;
    }

    union {
        FARPROC object;
        strlen_function function;
    } converter;
    converter.object = GetProcAddress(handle, "strlen");
    if (converter.function == NULL) {
        FreeLibrary(handle);
        return -1;
    }

    int result = (int)converter.function("hello");
    FreeLibrary(handle);
    return result;
}

int main(void)
{
    CLINGS_CHECK_INT(dynamic_strlen(), 5);
    return clings_report();
}
'''.lstrip()

_DYNAMIC_LINKING_EXERCISE = _DYNAMIC_LINKING_SOLUTION.replace(
    '    converter.object = GetProcAddress(handle, "strlen");\n',
    "    /* TODO: look up the strlen symbol. */\n"
    '    converter.object = GetProcAddress(handle, "strlen_missing");\n',
)

_NORETURN_SOLUTION = r'''
/*
 * clings exercise: 19_modern_c_library/01_noreturn
 * title: _Noreturn functions
 * objective: Declare a function that never returns and observe its exit status.
 * hint: The child re-runs this program with the "child" argument, then exits with status 7.
 */

#include "clings/test.h"

#include <process.h>
#include <stdnoreturn.h>
#include <stdlib.h>
#include <string.h>

_Noreturn void terminate_now(void)
{
    exit(7);
}

int run_noreturn(int argc, char **argv)
{
    if (argc > 1 && strcmp(argv[1], "child") == 0) {
        terminate_now();
    }

    /* Windows has no fork(); the child is this same executable, re-run with a
     * marker argument so it can tell the two roles apart. */
    const char *child_args[] = {argv[0], "child", NULL};
    intptr_t child = _spawnv(_P_NOWAIT, argv[0], child_args);
    if (child == -1) {
        return 0;
    }

    int status = 0;
    if (_cwait(&status, child, _WAIT_CHILD) == -1) {
        return 0;
    }
    return status == 7;
}

int main(int argc, char **argv)
{
    CLINGS_CHECK_INT(run_noreturn(argc, argv), 1);
    return clings_report();
}
'''.lstrip()

_NORETURN_EXERCISE = _NORETURN_SOLUTION.replace(
    "_Noreturn void terminate_now(void)\n{\n    exit(7);\n}\n",
    "_Noreturn void terminate_now(void)\n{\n"
    "    /* TODO: terminate with status 7. */\n    _Exit(0);\n}\n",
)

WHOLE_FILE: dict[str, dict[str, str]] = {
    "17_translation_units/05_dynamic_linking": {
        "solution": _DYNAMIC_LINKING_SOLUTION,
        "exercise": _DYNAMIC_LINKING_EXERCISE,
    },
    "19_modern_c_library/01_noreturn": {
        "solution": _NORETURN_SOLUTION,
        "exercise": _NORETURN_EXERCISE,
    },
}

# Applied to the initial exercise and the template, never to the solution.
# Use this when the upstream break is only broken on some platforms: the
# solution stays the same, the starting point is broken in a way that fails
# everywhere.
EXERCISE_ONLY: dict[str, list[tuple[str, str]]] = {
    # Upstream breaks this by returning "RAND_MAX == 32767", which is a lie on
    # glibc (2147483647) but the literal answer on the Microsoft CRT (32767),
    # so the exercise would start out passing.  Using ">" keeps the intended
    # lesson (the guaranteed minimum is inclusive) and still fails on Windows.
    "12_standard_library/15_rand_max": [
        ("    return RAND_MAX == 32767;\n", "    return RAND_MAX > 32767;\n"),
    ],
}


def rewritten_exercises() -> list[str]:
    """Every exercise ident that this module touches, for docs and reporting."""
    return sorted(set(SUBSTITUTIONS) | set(WHOLE_FILE) | set(EXERCISE_ONLY))


def _replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    occurrences = text.count(old)
    if occurrences != 1:
        raise SystemExit(
            f"windows override mismatch in {path}: expected 1 occurrence of\n"
            f"---\n{old}---\nfound {occurrences}"
        )
    path.write_text(text.replace(old, new), encoding="utf-8")


def apply(root: Path) -> None:
    """Apply every override to a freshly synced tree rooted at *root*."""
    for rel, replacements in SUBSTITUTIONS.items():
        targets = [
            root / "solutions" / f"{rel}.c",
            root / "exercises" / f"{rel}.c",
            root / "templates" / f"{rel}.c",
        ]
        for target in targets:
            if not target.is_file():
                raise SystemExit(f"windows override target missing: {target}")
            for old, new in replacements:
                _replace_once(target, old, new)

    for rel, replacements in EXERCISE_ONLY.items():
        for target in (
            root / "exercises" / f"{rel}.c",
            root / "templates" / f"{rel}.c",
        ):
            if not target.is_file():
                raise SystemExit(f"windows override target missing: {target}")
            for old, new in replacements:
                _replace_once(target, old, new)

    for rel, variants in WHOLE_FILE.items():
        pairs = [
            (root / "solutions" / f"{rel}.c", variants["solution"]),
            (root / "exercises" / f"{rel}.c", variants["exercise"]),
            (root / "templates" / f"{rel}.c", variants["exercise"]),
        ]
        for target, text in pairs:
            if not target.is_file():
                raise SystemExit(f"windows override target missing: {target}")
            target.write_text(text, encoding="utf-8")
