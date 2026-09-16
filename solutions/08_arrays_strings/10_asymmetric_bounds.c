/*
 * clings exercise: 08_arrays_strings/10_asymmetric_bounds
 * title: Asymmetric bounds
 * objective: Use the half-open interval [low, high).
 * hint: The upper bound is exclusive: value < high.
 */

#include "clings/test.h"

int in_range(int value, int low, int high)
{
    return value >= low && value < high;
}

int range_length(int low, int high)
{
    return high - low;
}

int loop_count(int low, int high)
{
    int count = 0;
    for (int value = low; value < high; ++value) {
        ++count;
    }
    return count;
}

int main(void)
{
    CLINGS_CHECK_INT(in_range(4, 0, 5), 1);
    CLINGS_CHECK_INT(in_range(5, 0, 5), 0);
    CLINGS_CHECK_INT(range_length(0, 5), 5);
    CLINGS_CHECK_INT(loop_count(0, 5), 5);
    return clings_report();
}
