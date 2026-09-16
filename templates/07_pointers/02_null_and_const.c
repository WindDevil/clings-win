/*
 * clings exercise: 07_pointers/02_null_and_const
 * title: NULL and const correctness
 * objective: Check for NULL and respect pointer-to-const.
 * hint: A pointer-to-const can read but not write the pointed-to object.
 */

#include "clings/test.h"

#include <stddef.h>

int is_null(const void *pointer)
{
    /* TODO: return true only for a null pointer. */
    return pointer != NULL;
}

int read_const(const int *value)
{
    return *value;
}

void write_through(int *value, int new_value)
{
    *value = new_value;
}

int main(void)
{
    int value = 5;

    CLINGS_CHECK_INT(is_null(NULL), 1);
    CLINGS_CHECK_INT(is_null(&value), 0);
    CLINGS_CHECK_INT(read_const(&value), 5);
    write_through(&value, 9);
    CLINGS_CHECK_INT(value, 9);
    return clings_report();
}
