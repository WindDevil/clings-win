/*
 * clings exercise: 15_ub_safety/03_out_of_bounds
 * title: Bounds checking
 * objective: Reject indices outside the logical array length.
 * hint: An index is invalid when it is less than zero or greater than or equal to count.
 */

#include "clings/test.h"

int get_or_default(const int *values, int count, int index, int fallback)
{
    if (index < 0 || index >= count) {
        return fallback;
    }
    return values[index];
}

int main(void)
{
    const int values[] = {10, 20, 30, 999};

    CLINGS_CHECK_INT(get_or_default(values, 3, 0, 123), 10);
    CLINGS_CHECK_INT(get_or_default(values, 3, 2, 123), 30);
    CLINGS_CHECK_INT(get_or_default(values, 3, 3, 123), 123);
    CLINGS_CHECK_INT(get_or_default(values, 3, -1, 123), 123);
    return clings_report();
}
