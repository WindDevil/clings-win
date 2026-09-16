/*
 * clings exercise: 07_pointers/04_pointer_to_pointer
 * title: Pointers to pointers
 * objective: Let a function allocate and update a caller-owned pointer.
 * hint: Assign through *slot, not to the local slot parameter.
 */

#include "clings/test.h"

#include <stdlib.h>

int allocate_int(int **out, int value)
{
    *out = malloc(sizeof **out);
    if (*out == NULL) {
        return -1;
    }
    **out = value;
    return 0;
}

void set_pointer(int **slot, int *value)
{
    /* TODO: update the pointer that slot points to. */
    slot = &value;
}

int main(void)
{
    int *allocated = NULL;
    int value = 5;
    int *slot = NULL;

    CLINGS_CHECK_INT(allocate_int(&allocated, 99), 0);
    CLINGS_CHECK(allocated != NULL);
    CLINGS_CHECK_INT(*allocated, 99);
    free(allocated);
    set_pointer(&slot, &value);
    CLINGS_CHECK(slot == &value);
    return clings_report();
}
