/*
 * clings exercise: 09_dynamic_memory/02_calloc
 * title: Zero-initialized allocation
 * objective: Use calloc when every byte must start as zero.
 * hint: calloc(count, size) returns zeroed memory.
 */

#include "clings/test.h"

#include <stdlib.h>

int *make_zeroed(size_t count)
{
    /* TODO: return zero-initialized storage. */
    int *values = malloc(count * sizeof(int));
    if (values != NULL) {
        for (size_t i = 0; i < count; ++i) {
            values[i] = 1;
        }
    }
    return values;
}

int main(void)
{
    int *values = make_zeroed(5);

    CLINGS_CHECK(values != NULL);
    for (int i = 0; i < 5; ++i) {
        CLINGS_CHECK_INT(values[i], 0);
    }
    free(values);
    return clings_report();
}
