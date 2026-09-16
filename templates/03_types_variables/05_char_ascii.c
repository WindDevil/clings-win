/*
 * clings 练习: 03_types_variables/05_char_ascii
 * title: 字符与 ASCII
 * objective: 处理 char 值，并使用 ctype 的字符分类函数。
 * hint: 小写字母连续，这个性质只对执行字符集成立。
 */

#include "clings/test.h"

#include <ctype.h>

int is_ascii_digit(char c)
{
    return c >= '0' && c <= '9';
}

char to_upper_ascii(char c)
{
    /* TODO: 把小写字母转成大写。 */
    return (c >= 'A' && c <= 'Z') ? (char)(c - 'A' + 'a') : c;
}

int main(void)
{
    CLINGS_CHECK_INT(is_ascii_digit('7'), 1);
    CLINGS_CHECK_INT(is_ascii_digit('x'), 0);
    CLINGS_CHECK_INT(to_upper_ascii('q'), 'Q');
    CLINGS_CHECK_INT(to_upper_ascii('Z'), 'Z');
    CLINGS_CHECK_INT(to_upper_ascii('!'), '!');
    return clings_report();
}
