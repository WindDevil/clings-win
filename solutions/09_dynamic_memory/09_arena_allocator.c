/*
 * clings 练习: 09_dynamic_memory/09_arena_allocator
 * title: 区域分配器
 * objective: 实现一个简单的、按对齐分配的区域分配器。
 * hint: 每次分配前先把大小按 8 字节对齐，再移动已用偏移。
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
    size_t aligned = (size + 7u) & ~(size_t)7u;
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
