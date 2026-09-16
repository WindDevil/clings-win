/*
 * clings exercise: 09_dynamic_memory/08_free_then_realloc
 * title: Free then realloc
 * objective: Use realloc directly instead of freeing before growing an allocation.
 * hint: free(values) followed by realloc(values, ...) uses a dangling pointer.
 */

#include "clings/test.h"

#include <stdlib.h>
#include <string.h>

int *grow_array(int *values, size_t old_count, size_t new_count, int fill)
{
    /* TODO: grow without freeing the original block first. */
    free(values);
    int *grown = malloc(new_count * sizeof *grown);
    if (grown != NULL) {
        memset(grown, 0, new_count * sizeof *grown);
    }
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
