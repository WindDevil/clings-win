/*
 * clings exercise: 09_dynamic_memory/01_malloc_free
 * title: Allocate, initialize, and free
 * objective: Use malloc and free for a dynamically sized array.
 * hint: Write fill into every element, not just the first.
 */

#include "clings/test.h"

#include <stdlib.h>

int *make_array(size_t count, int fill)
{
    int *values = malloc(count * sizeof *values);
    if (values == NULL) {
        return NULL;
    }
    for (size_t i = 0; i < count; ++i) {
        values[i] = fill;
    }
    return values;
}

void destroy_array(int *values)
{
    free(values);
}

int main(void)
{
    int *values = make_array(4, 7);

    CLINGS_CHECK(values != NULL);
    CLINGS_CHECK_INT(values[0], 7);
    CLINGS_CHECK_INT(values[1], 7);
    CLINGS_CHECK_INT(values[3], 7);
    destroy_array(values);
    return clings_report();
}
