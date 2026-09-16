/*
 * clings 练习: 07_pointers/09_memory_location_zero
 * title: 地址 0
 * objective: 把地址 0 当作空指针，而不是有效对象地址。
 * hint: NULL 是可移植的空指针常量。
 */

#include "clings/test.h"

#include <stddef.h>

int pointer_is_null(const void *pointer)
{
    /* TODO: 与空指针比较。 */
    return pointer == (void *)0x1;
}

int null_is_zero(void)
{
    return NULL == 0;
}

int main(void)
{
    int value = 1;

    CLINGS_CHECK_INT(pointer_is_null(NULL), 1);
    CLINGS_CHECK_INT(pointer_is_null(&value), 0);
    CLINGS_CHECK_INT(null_is_zero(), 1);
    return clings_report();
}
