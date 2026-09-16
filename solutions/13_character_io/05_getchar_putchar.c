/*
 * clings 练习: 13_character_io/05_getchar_putchar
 * title: getchar 与 putchar
 * objective: 直接使用标准的输入输出字符宏。
 * hint: 测试时可以用 ungetc 把一个字符退回 stdin。
 */

#include "clings/test.h"

#include <stdio.h>

int read_one_character(void)
{
    return getchar();
}

int write_one_character(int character)
{
    return putchar(character);
}

int main(void)
{
    CLINGS_CHECK_INT(ungetc('x', stdin), 'x');
    CLINGS_CHECK_INT(read_one_character(), 'x');
    CLINGS_CHECK_INT(write_one_character('y'), 'y');
    return clings_report();
}
