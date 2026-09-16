/*
 * clings exercise: 15_ub_safety/04_use_after_free
 * title: Use-after-free
 * objective: Clear a pointer after freeing its target.
 * hint: Write NULL through the pointer-to-pointer after free.
 */

#include "clings/test.h"

#include <stdlib.h>

void free_and_clear(int **pointer)
{
    free(*pointer);
    /* TODO: clear the caller's pointer. */
}

int is_null(const void *pointer)
{
    return pointer == NULL;
}

int main(void)
{
    int *value = malloc(sizeof *value);

    CLINGS_CHECK(value != NULL);
    *value = 7;
    free_and_clear(&value);
    CLINGS_CHECK_INT(is_null(value), 1);
    return clings_report();
}
