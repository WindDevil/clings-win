/*
 * clings 练习: 10_aggregates/08_container_of
 * title: offsetof 与 container_of
 * objective: 由成员指针反推出外层结构体。
 * hint: 减去内层成员的字节偏移。
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
