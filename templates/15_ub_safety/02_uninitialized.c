/*
 * clings exercise: 15_ub_safety/02_uninitialized
 * title: Initialize before use
 * objective: Give every local variable a defined initial value.
 * hint: Start result at -1 so the fallback path is well-defined.
 */

#include "clings/test.h"

int initialized_or_default(int value)
{
    /* TODO: initialize the fallback value. */
    int result = 12345;
    if (value > 0) {
        result = value;
    }
    return result;
}

int main(void)
{
    CLINGS_CHECK_INT(initialized_or_default(0), -1);
    CLINGS_CHECK_INT(initialized_or_default(-5), -1);
    CLINGS_CHECK_INT(initialized_or_default(7), 7);
    return clings_report();
}
