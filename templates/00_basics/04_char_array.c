/*
 * clings 练习: 00_basics/04_char_array
 * title: 字符数组
 * objective: 把文本存进 char 数组，并访问其中字符。
 * hint: 数组下标从 0 开始；sizeof("hello") 包含结尾的 NUL。
 */

#include "clings/test.h"

char text[] = "hello";

char first_character(void)
{
    return text[0];
}

char last_character(void)
{
    /* TODO: 返回最后一个可见字符，不是结尾的 NUL。 */
    return text[5];
}

int main(void)
{
    CLINGS_CHECK_INT(first_character(), 'h');
    CLINGS_CHECK_INT(last_character(), 'o');
    return clings_report();
}
