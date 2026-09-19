/*
 * clings 练习: 00_basics/02_printf_values
 * title: 打印一个值
 * objective: 用 printf 的 %d 打印一个整数。
 * hint: int 实参用 %d，并且把换行写进格式串。
 */

#include "clings/test.h"

#include <stdio.h>

int print_value(int value)
{
    /* TODO: 打印这个整数值并换行。 */
    return printf("value\n");
}

int main(void)
{
    CLINGS_CHECK_STDOUT(print_value(42), "42\n");
    CLINGS_CHECK_STDOUT(print_value(7), "7\n");
    CLINGS_CHECK_STDOUT(print_value(-1234), "-1234\n");
    return clings_report();
}
