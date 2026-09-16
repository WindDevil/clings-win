/*
 * clings exercise: 09_dynamic_memory/03_realloc
 * title: Growing an allocation
 * objective: Use realloc safely and initialize only the new elements.
 * hint: Start filling at old_count so the existing elements survive.
 */

#include "clings/test.h"

#include <stdlib.h>

int *grow_array(int *values, size_t old_count, size_t new_count, int fill)
{
    int *grown = realloc(values, new_count * sizeof *grown);
    if (grown == NULL) {
        return NULL;
    }
    for (size_t i = old_count; i < new_count; ++i) {
        grown[i] = fill;
    }
    return grown;
}

int main(void)
{
    int *values = malloc(2 * sizeof *values);
    values[0] = 10;
    values[1] = 20;

    values = grow_array(values, 2, 5, 9);
    CLINGS_CHECK(values != NULL);
    CLINGS_CHECK_INT(values[0], 10);
    CLINGS_CHECK_INT(values[1], 20);
    CLINGS_CHECK_INT(values[2], 9);
    CLINGS_CHECK_INT(values[4], 9);
    free(values);
    return clings_report();
}
