/*
 * clings exercise: 07_pointers/01_pointer_basics
 * title: Dereference and address-of
 * objective: Read and write through pointers.
 * hint: Assigning the parameter itself does not modify the caller's variable.
 */

#include "clings/test.h"

int read_through(const int *value)
{
    return *value;
}

void write_through(int *value, int new_value)
{
    /* TODO: write through the pointer, not to the local parameter. */
    value = &new_value;
}

int main(void)
{
    int value = 7;

    CLINGS_CHECK_INT(read_through(&value), 7);
    write_through(&value, 42);
    CLINGS_CHECK_INT(value, 42);
    return clings_report();
}
