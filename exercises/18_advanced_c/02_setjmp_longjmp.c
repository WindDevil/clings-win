/*
 * clings exercise: 18_advanced_c/02_setjmp_longjmp
 * title: setjmp and longjmp
 * objective: Use non-local jumps for a simple error path.
 * hint: longjmp returns control to the matching setjmp call.
 */

#include "clings/test.h"

#include <setjmp.h>

static jmp_buf jump_buffer;

static int checked_positive(int value)
{
    if (value < 0) {
        /* TODO: jump back to the setjmp call. */
        return -1;
    }
    return value;
}

int run_checked(int value, int *out)
{
    if (setjmp(jump_buffer) != 0) {
        return -1;
    }
    *out = checked_positive(value);
    return 0;
}

int main(void)
{
    int out = 0;

    CLINGS_CHECK_INT(run_checked(5, &out), 0);
    CLINGS_CHECK_INT(out, 5);
    CLINGS_CHECK_INT(run_checked(-1, &out), -1);
    return clings_report();
}
