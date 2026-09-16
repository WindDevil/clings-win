/*
 * clings exercise: 07_pointers/07_pointer_to_array
 * title: Pointers to arrays and &array
 * objective: Distinguish a pointer to an array from a pointer to its first element.
 * hint: &a + 1 advances by the whole array, not by one element.
 */

#include "clings/test.h"

#include <stddef.h>

int sum_row(const int (*row)[4])
{
    int sum = 0;
    for (int i = 0; i < 4; ++i) {
        sum += (*row)[i];
    }
    return sum;
}

int pointer_to_array_difference(void)
{
    int values[4] = {0};
    /* TODO: advance by the whole array, not one element. */
    return (int)((char *)(values + 1) - (char *)values);
}

int main(void)
{
    const int row[4] = {1, 2, 3, 4};

    CLINGS_CHECK_INT(sum_row(&row), 10);
    CLINGS_CHECK_INT(pointer_to_array_difference(), (int)(sizeof(int) * 4));
    return clings_report();
}
