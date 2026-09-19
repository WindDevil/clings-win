/*
 * clings 练习: 00_basics/01_printf
 * title: 用 printf 打印
 * objective: 用 printf 打印一行文本。
 * hint: printf 返回打印出的字符数，包含换行符。
 */

#include "clings/test.h"

#include <stdio.h>

int print_greeting(void)
{
    /* TODO: 打印 Hello, C! 并换行。 */
    return printf("Hello, world!\n");
}

int main(void)
{
    CLINGS_CHECK_STDOUT(print_greeting(), "Hello, C!\n");
    return clings_report();
}
