/*
 * clings exercise: 09_dynamic_memory/04_memory_leak
 * title: Detecting a memory leak
 * objective: Pair every allocation with a matching free.
 * hint: The cleanup path must release the tracked allocation.
 */

#include "clings/test.h"

#include <stdlib.h>

static size_t outstanding_allocations = 0;

static void *tracked_malloc(size_t size)
{
    void *pointer = malloc(size);
    if (pointer != NULL) {
        ++outstanding_allocations;
    }
    return pointer;
}

static void tracked_free(void *pointer)
{
    if (pointer != NULL) {
        --outstanding_allocations;
    }
    free(pointer);
}

size_t outstanding(void)
{
    return outstanding_allocations;
}

int sum_and_free(const int *values, int count, int *out)
{
    int *copy = tracked_malloc((size_t)count * sizeof *copy);
    if (copy == NULL) {
        return -1;
    }

    int sum = 0;
    for (int i = 0; i < count; ++i) {
        copy[i] = values[i];
        sum += copy[i];
    }
    *out = sum;

    /* TODO: release the tracked allocation. */
    return 0;
}

int main(void)
{
    const int values[] = {1, 2, 3};
    int out = 0;

    CLINGS_CHECK_INT(outstanding(), 0);
    CLINGS_CHECK_INT(sum_and_free(values, 3, &out), 0);
    CLINGS_CHECK_INT(out, 6);
    CLINGS_CHECK_INT(outstanding(), 0);
    return clings_report();
}
