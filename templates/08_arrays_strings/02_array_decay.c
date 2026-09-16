/*
 * clings exercise: 08_arrays_strings/02_array_decay
 * title: Array-to-pointer decay
 * objective: See how an array parameter becomes a pointer.
 * hint: Inside a function, an array parameter has pointer type.
 */

#include "clings/test.h"

int local_array_length(void)
{
    int values[10];
    /* TODO: use the local array, not a pointer, to compute the length. */
    return (int)(sizeof(values) / sizeof(int *));
}

int parameter_is_pointer(const int *values)
{
    return sizeof(values) == sizeof(int *);
}

int main(void)
{
    int values[4] = {0};

    CLINGS_CHECK_INT(local_array_length(), 10);
    CLINGS_CHECK_INT(parameter_is_pointer(values), 1);
    return clings_report();
}
