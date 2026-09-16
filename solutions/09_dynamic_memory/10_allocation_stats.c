/*
 * clings exercise: 09_dynamic_memory/10_allocation_stats
 * title: Allocation statistics
 * objective: Track outstanding allocations with wrapped malloc and free.
 * hint: Increment the free counter when a non-NULL pointer is freed.
 */

#include "clings/test.h"

#include <stddef.h>
#include <stdlib.h>

static size_t allocations = 0;
static size_t frees = 0;

void *tracked_malloc(size_t size)
{
    void *pointer = malloc(size);
    if (pointer != NULL) {
        ++allocations;
    }
    return pointer;
}

void tracked_free(void *pointer)
{
    if (pointer != NULL) {
        ++frees;
    }
    free(pointer);
}

size_t outstanding_allocations(void)
{
    return allocations - frees;
}

int main(void)
{
    void *first = tracked_malloc(1);
    void *second = tracked_malloc(2);

    CLINGS_CHECK_INT(outstanding_allocations(), 2);
    tracked_free(first);
    CLINGS_CHECK_INT(outstanding_allocations(), 1);
    tracked_free(second);
    CLINGS_CHECK_INT(outstanding_allocations(), 0);
    return clings_report();
}
