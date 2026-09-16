/*
 * clings exercise: 06_functions/04_static_inline
 * title: Internal linkage and inline helpers
 * objective: Use static functions and file-scope state.
 * hint: Update call_count before returning the incremented value.
 */

#include "clings/test.h"

static int call_count = 0;

static int add_one(int value)
{
    /* TODO: count every call. */
    return value + 1;
}

int call_add_one(int value)
{
    return add_one(value);
}

int add_one_calls(void)
{
    return call_count;
}

int main(void)
{
    CLINGS_CHECK_INT(add_one_calls(), 0);
    CLINGS_CHECK_INT(call_add_one(1), 2);
    CLINGS_CHECK_INT(call_add_one(2), 3);
    CLINGS_CHECK_INT(add_one_calls(), 2);
    return clings_report();
}
