/*
 * clings exercise: 08_arrays_strings/01_array_basics
 * title: Array traversal
 * objective: Iterate over an array and compute a sum and maximum.
 * hint: Use values[i] inside the loop, not values[0].
 */

#include "clings/test.h"

int array_sum(const int *values, int count)
{
    int sum = 0;
    for (int i = 0; i < count; ++i) {
        /* TODO: add the current element. */
        sum += values[0];
    }
    return sum;
}

int array_max(const int *values, int count)
{
    int maximum = values[0];
    for (int i = 1; i < count; ++i) {
        if (values[i] > maximum) {
            maximum = values[i];
        }
    }
    return maximum;
}

int main(void)
{
    const int values[] = {3, -1, 7, 2};

    CLINGS_CHECK_INT(array_sum(values, 4), 11);
    CLINGS_CHECK_INT(array_max(values, 4), 7);
    return clings_report();
}
