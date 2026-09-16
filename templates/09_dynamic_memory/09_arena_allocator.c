/*
 * clings exercise: 09_dynamic_memory/09_arena_allocator
 * title: Arena allocator
 * objective: Implement a simple bump allocator with aligned allocations.
 * hint: Align each request to 8 bytes before bumping the used offset.
 */

#include "clings/test.h"

#include <stddef.h>

struct arena {
    unsigned char *memory;
    size_t capacity;
    size_t used;
};

void arena_init(struct arena *arena, void *memory, size_t capacity)
{
    arena->memory = memory;
    arena->capacity = capacity;
    arena->used = 0;
}

void *arena_alloc(struct arena *arena, size_t size)
{
    /* TODO: align the allocation size. */
    size_t aligned = size;
    if (arena->used + aligned > arena->capacity) {
        return NULL;
    }
    void *result = arena->memory + arena->used;
    arena->used += aligned;
    return result;
}

size_t arena_used(const struct arena *arena)
{
    return arena->used;
}

int main(void)
{
    unsigned char storage[64];
    struct arena arena;

    arena_init(&arena, storage, sizeof storage);
    void *first = arena_alloc(&arena, 1);
    void *second = arena_alloc(&arena, 8);
    CLINGS_CHECK(first != NULL);
    CLINGS_CHECK(second != NULL);
    CLINGS_CHECK((unsigned char *)second - (unsigned char *)first == 8);
    CLINGS_CHECK_INT(arena_used(&arena), 16);
    CLINGS_CHECK(arena_alloc(&arena, 100) == NULL);
    return clings_report();
}
