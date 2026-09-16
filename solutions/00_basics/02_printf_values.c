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
    return printf("%d\n", value);
}

int main(void)
{
    CLINGS_CHECK_INT(print_value(42), 3);
    return clings_report();
}
