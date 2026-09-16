/*
 * clings exercise: 10_aggregates/08_container_of
 * title: offsetof and container_of
 * objective: Recover an outer struct from a pointer to one of its members.
 * hint: Subtract the byte offset of the inner member.
 */

#include "clings/test.h"

#include <stddef.h>

struct inner {
    int value;
};

struct outer {
    int id;
    struct inner inner;
};

struct outer *outer_from_inner(struct inner *inner)
{
    return (struct outer *)((char *)inner - offsetof(struct outer, inner));
}

int main(void)
{
    struct outer outer = {.id = 42, .inner = {.value = 7}};
    struct outer *recovered = outer_from_inner(&outer.inner);

    CLINGS_CHECK(recovered == &outer);
    CLINGS_CHECK_INT(recovered->id, 42);
    CLINGS_CHECK_INT(recovered->inner.value, 7);
    return clings_report();
}
