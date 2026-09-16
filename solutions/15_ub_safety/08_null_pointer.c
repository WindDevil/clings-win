/*
 * clings 练习: 15_ub_safety/08_null_pointer
 * title: 空指针检查
 * objective: 绝不解引用空指针。
 * hint: 用条件表达式给出兜底值。
 */

#include "clings/test.h"

#include <stddef.h>

int dereference_or_default(const int *pointer, int fallback)
{
    return pointer != NULL ? *pointer : fallback;
}

int main(void)
{
    int value = 42;

    CLINGS_CHECK_INT(dereference_or_default(&value, -1), 42);
    CLINGS_CHECK_INT(dereference_or_default(NULL, -1), -1);
    return clings_report();
}
