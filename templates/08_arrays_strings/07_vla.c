/*
 * clings exercise: 08_arrays_strings/07_vla
 * title: Variable-length arrays
 * objective: Create an array whose length is a runtime value.
 * hint: A VLA is declared with a runtime expression: int values[n].
 */

#include "clings/test.h"

int sum_vla(int count)
{
    int values[count];
    for (int i = 0; i < count; ++i) {
        /* TODO: initialize the VLA element. */
        values[i] = 1;
    }
    int sum = 0;
    for (int i = 0; i < count; ++i) {
        sum += values[i];
    }
    return sum;
}

int main(void)
{
    CLINGS_CHECK_INT(sum_vla(1), 1);
    CLINGS_CHECK_INT(sum_vla(4), 10);
    CLINGS_CHECK_INT(sum_vla(10), 55);
    return clings_report();
}
