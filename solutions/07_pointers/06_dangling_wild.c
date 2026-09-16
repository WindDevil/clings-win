/*
 * clings exercise: 07_pointers/06_dangling_wild
 * title: Dangling pointers and safe free
 * objective: Set a freed pointer to NULL to prevent accidental reuse.
 * hint: After free(*pointer), assign NULL through the pointer-to-pointer.
 */

#include "clings/test.h"

#include <stdlib.h>

void safe_free(int **pointer)
{
    free(*pointer);
    *pointer = NULL;
}

int is_null(const void *pointer)
{
    return pointer == NULL;
}

int main(void)
{
    int *value = malloc(sizeof *value);

    CLINGS_CHECK(value != NULL);
    *value = 42;
    safe_free(&value);
    CLINGS_CHECK_INT(is_null(value), 1);
    return clings_report();
}
