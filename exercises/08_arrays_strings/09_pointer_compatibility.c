/*
 * clings exercise: 08_arrays_strings/09_pointer_compatibility
 * title: Pointer compatibility and const
 * objective: Pass a non-const array through a pointer-to-const.
 * hint: A pointer to const may point at non-const data.
 */

#include "clings/test.h"

#include <stddef.h>

int sum_const(const int *values, size_t count)
{
    int sum = 0;
    for (size_t i = 0; i < count; ++i) {
        sum += values[i];
    }
    return sum;
}

int pointer_compatibility(void)
{
    int values[3] = {1, 2, 3};
    const int *pointer = values;
    /* TODO: pass the full length through the const pointer. */
    return sum_const(pointer, 2);
}

int main(void)
{
    const int const_values[3] = {4, 5, 6};

    CLINGS_CHECK_INT(pointer_compatibility(), 6);
    CLINGS_CHECK_INT(sum_const(const_values, 3), 15);
    return clings_report();
}
