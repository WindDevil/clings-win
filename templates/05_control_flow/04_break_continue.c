/*
 * clings exercise: 05_control_flow/04_break_continue
 * title: break and continue
 * objective: Use break to stop early and continue to skip one iteration.
 * hint: continue skips the rest of the current iteration; break exits the loop.
 */

#include "clings/test.h"

int first_multiple_of_three(int limit)
{
    for (int value = 1; value <= limit; ++value) {
        if (value % 3 == 0) {
            return value;
        }
    }
    return -1;
}

int sum_skipping_multiples_of_three(int limit)
{
    int sum = 0;
    for (int value = 1; value <= limit; ++value) {
        if (value % 3 == 0) {
            /* TODO: skip this value, do not stop the loop. */
            break;
        }
        sum += value;
    }
    return sum;
}

int main(void)
{
    CLINGS_CHECK_INT(first_multiple_of_three(10), 3);
    CLINGS_CHECK_INT(sum_skipping_multiples_of_three(5), 12);
    CLINGS_CHECK_INT(sum_skipping_multiples_of_three(0), 0);
    return clings_report();
}
