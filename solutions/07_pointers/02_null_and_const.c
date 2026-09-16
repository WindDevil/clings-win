/*
 * clings 练习: 07_pointers/02_null_and_const
 * title: NULL 与 const 正确性
 * objective: 检查 NULL，并尊重指向 const 的指针。
 * hint: 指向 const 的指针能读，但不能写它指向的对象。
 */

#include "clings/test.h"

#include <stddef.h>

int is_null(const void *pointer)
{
    return pointer == NULL;
}

int read_const(const int *value)
{
    return *value;
}

void write_through(int *value, int new_value)
{
    *value = new_value;
}

int main(void)
{
    int value = 5;

    CLINGS_CHECK_INT(is_null(NULL), 1);
    CLINGS_CHECK_INT(is_null(&value), 0);
    CLINGS_CHECK_INT(read_const(&value), 5);
    write_through(&value, 9);
    CLINGS_CHECK_INT(value, 9);
    return clings_report();
}
