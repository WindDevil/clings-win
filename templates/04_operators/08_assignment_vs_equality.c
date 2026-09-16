/*
 * clings exercise: 04_operators/08_assignment_vs_equality
 * title: Assignment versus equality
 * objective: Use == for comparison and recognize the = versus == trap.
 * hint: A single = assigns; a double == compares.
 */

#include "clings/test.h"

int is_equal(int left, int right)
{
    /* TODO: compare instead of assign. */
    return left = right;
}

int compare_with_zero(int value)
{
    if (value == 0) {
        return 1;
    }
    return 0;
}

int main(void)
{
    CLINGS_CHECK_INT(is_equal(1, 1), 1);
    CLINGS_CHECK_INT(is_equal(1, 2), 0);
    CLINGS_CHECK_INT(compare_with_zero(0), 1);
    CLINGS_CHECK_INT(compare_with_zero(5), 0);
    return clings_report();
}
