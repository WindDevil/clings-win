/*
 * clings exercise: 06_functions/06_tail_recursion
 * title: Tail recursion
 * objective: Rewrite a recursive sum using an accumulator.
 * hint: The recursive call should be the last operation.
 */

#include "clings/test.h"

static int sum_tail(int value, int accumulator)
{
    return value == 0 ? accumulator : /* TODO: add the current value to the accumulator. */
        sum_tail(value - 1, accumulator);
}

int sum_tail_wrapper(int value)
{
    return sum_tail(value, 0);
}

int main(void)
{
    CLINGS_CHECK_INT(sum_tail_wrapper(0), 0);
    CLINGS_CHECK_INT(sum_tail_wrapper(5), 15);
    CLINGS_CHECK_INT(sum_tail_wrapper(10), 55);
    return clings_report();
}
