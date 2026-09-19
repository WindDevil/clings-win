/*
 * clings 练习: 00_basics/09_compiler_diagnostics
 * title: 读懂编译器诊断
 * objective: 修掉编译器报出的格式串警告。
 * hint: 打印 int 用 %d；%s 要的是字符串。
 */

#include "clings/test.h"

#include <stdio.h>

int print_number(int value)
{
    /* TODO: 用 int 对应的转换说明符。 */
    return printf("%s\n", value);
}

int main(void)
{
    CLINGS_CHECK_STDOUT(print_number(42), "42\n");
    return clings_report();
}
