/*
 * clings 练习: 03_types_variables/06_storage_scope
 * title: 存储类与作用域
 * objective: 观察静态变量的生存期与块作用域。
 * hint: ++counter 先自增；counter++ 返回旧值。
 */

#include "clings/test.h"

static int counter = 0;

int next_counter(void)
{
    /* TODO: 前置自增这个 static 计数器。 */
    return counter++;
}

int local_shadow(int value)
{
    int local_counter = value;
    return local_counter;
}

int main(void)
{
    CLINGS_CHECK_INT(next_counter(), 1);
    CLINGS_CHECK_INT(next_counter(), 2);
    CLINGS_CHECK_INT(local_shadow(99), 99);
    CLINGS_CHECK_INT(next_counter(), 3);
    return clings_report();
}
