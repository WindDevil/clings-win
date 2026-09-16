/*
 * clings exercise: 07_pointers/10_one_past_pointer
 * title: One-past pointer arithmetic
 * objective: Do not treat a pointer to a single object as an array.
 * hint: For a single object, only the one-past pointer is valid; do not dereference it.
 */

#include "clings/test.h"

int one_past_offset(void)
{
    int value = 42;
    int *pointer = &value;
    int *one_past = pointer + 1;
    return (int)(one_past - pointer);
}

int single_object_value(void)
{
    int value = 42;
    int *pointer = &value;
    return *pointer;
}

int main(void)
{
    CLINGS_CHECK_INT(one_past_offset(), 1);
    CLINGS_CHECK_INT(single_object_value(), 42);
    return clings_report();
}
