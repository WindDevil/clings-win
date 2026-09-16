/*
 * clings exercise: 07_pointers/12_pass_by_pointer
 * title: Pass by value and pass by pointer
 * objective: Modify caller-owned data through pointers.
 * hint: Save *a before overwriting it.
 */

#include "clings/test.h"

void swap_int(int *a, int *b)
{
    /* TODO: swap the two integers without losing either value. */
    *a = *b;
    *b = *a;
}

void increment_all(int *values, int count)
{
    for (int i = 0; i < count; ++i) {
        ++values[i];
    }
}

int main(void)
{
    int a = 1;
    int b = 2;
    int values[] = {1, 2, 3};

    swap_int(&a, &b);
    CLINGS_CHECK_INT(a, 2);
    CLINGS_CHECK_INT(b, 1);
    increment_all(values, 3);
    CLINGS_CHECK_INT(values[0], 2);
    CLINGS_CHECK_INT(values[1], 3);
    CLINGS_CHECK_INT(values[2], 4);
    return clings_report();
}
