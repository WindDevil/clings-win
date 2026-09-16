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
    /* TODO: terminate with status 7. */
    _Exit(0);
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
