/*
 * clings exercise: 03_types_variables/06_storage_scope
 * title: Storage classes and scope
 * objective: Observe the lifetime of a static variable and block scope.
 * hint: ++counter increments first; counter++ returns the old value.
 */

#include "clings/test.h"

static int counter = 0;

int next_counter(void)
{
    return ++counter;
}

int local_shadow(int value)
{
    int local_counter = value;
    return local_counter;
}

int main(void)
{
    CLINGS_CHECK_INT(next_counter(), 1);
    CLINGS_CHECK_INT(next_counter(), 2);
    CLINGS_CHECK_INT(local_shadow(99), 99);
    CLINGS_CHECK_INT(next_counter(), 3);
    return clings_report();
}
