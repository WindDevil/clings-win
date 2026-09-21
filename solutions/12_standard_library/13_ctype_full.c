/*
 * clings 练习: 12_standard_library/13_ctype_full
 * title: ctype.h 的字符分类与转换
 * objective: 把参数转成 unsigned char 后再传给 isalnum 和 toupper。
 * hint: 传给 ctype 函数的参数要转成 (unsigned char)，避免出现负值。
 */

#include "clings/test.h"

#include <ctype.h>

int count_alnum(const char *text)
{
    int count = 0;
    for (const char *pointer = text; *pointer != '\0'; ++pointer) {
        if (isalnum((unsigned char)*pointer)) {
            ++count;
        }
    }
    return count;
}

char upper_char(char character)
{
    return (char)toupper((unsigned char)character);
}

int main(void)
{
    CLINGS_CHECK_INT(count_alnum("a1 B2!"), 4);
    CLINGS_CHECK_INT(upper_char('q'), 'Q');
    CLINGS_CHECK_INT(upper_char('Z'), 'Z');
    return clings_report();
}
