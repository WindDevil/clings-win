/*
 * clings exercise: 03_types_variables/03_overflow
 * title: Unsigned wrap and checked signed addition
 * objective: Understand modulo wrap and avoid signed integer overflow.
 * hint: Check INT_MAX - b before adding b to a.
 */

#include "clings/test.h"

#include <limits.h>

unsigned wrap_add(unsigned a, unsigned b)
{
    return a + b;
}

int add_overflows(int a, int b)
{
    if (b > 0 && a > INT_MAX - b) {
        return 1;
    }
    if (b < 0 && a < INT_MIN - b) {
        return 1;
    }
    return 0;
}

long add_wide(int a, int b)
{
    return (long)a + (long)b;
}

int main(void)
{
    CLINGS_CHECK_INT(wrap_add(UINT_MAX, 1u), 0);
    CLINGS_CHECK_INT(add_overflows(INT_MAX, 1), 1);
    CLINGS_CHECK_INT(add_overflows(INT_MIN, -1), 1);
    CLINGS_CHECK_INT(add_overflows(2, 3), 0);
    CLINGS_CHECK_INT(add_wide(2, 3), 5);
    return clings_report();
}
