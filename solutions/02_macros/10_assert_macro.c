/*
 * clings exercise: 02_macros/10_assert_macro
 * title: Assertions and defensive programming
 * objective: Use assert for programmer errors and return values for user errors.
 * hint: A zero denominator is a normal error, so return -1 instead of dividing.
 */

#include "clings/test.h"

#include <assert.h>
#include <stddef.h>

int checked_divide(int numerator, int denominator, int *out)
{
    assert(out != NULL);
    if (denominator == 0) {
        return -1;
    }
    *out = numerator / denominator;
    return 0;
}

int main(void)
{
    int out = 0;

    CLINGS_CHECK_INT(checked_divide(10, 2, &out), 0);
    CLINGS_CHECK_INT(out, 5);
    CLINGS_CHECK_INT(checked_divide(10, 0, &out), -1);
    return clings_report();
}
