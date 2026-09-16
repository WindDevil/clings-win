/*
 * clings exercise: 15_ub_safety/08_null_pointer
 * title: Null pointer checks
 * objective: Never dereference a null pointer.
 * hint: Use a conditional expression to provide a fallback.
 */

#include "clings/test.h"

#include <stddef.h>

int dereference_or_default(const int *pointer, int fallback)
{
    return pointer != NULL ? *pointer : fallback;
}

int main(void)
{
    int value = 42;

    CLINGS_CHECK_INT(dereference_or_default(&value, -1), 42);
    CLINGS_CHECK_INT(dereference_or_default(NULL, -1), -1);
    return clings_report();
}
