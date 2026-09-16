/*
 * clings 练习: 08_arrays_strings/04_string_literals
 * title: 字符串字面量与可变字符串
 * objective: 扫描 const 字符串，修改可变的 char 数组。
 * hint: 字符串字面量不能改；char 数组可以改。
 */

#include "clings/test.h"

int count_vowels(const char *text)
{
    int count = 0;
    for (const char *p = text; *p != '\0'; ++p) {
        switch (*p) {
        case 'a':
        case 'e':
        case 'i':
        case 'o':
        case 'u':
            ++count;
            break;
        default:
            break;
        }
    }
    return count;
}

void replace_char(char *text, char from, char to)
{
    for (char *p = text; *p != '\0'; ++p) {
        if (*p == from) {
            /* TODO: 替换这个字符。 */
        }
    }
}

int main(void)
{
    char text[] = "hello";

    CLINGS_CHECK_INT(count_vowels("hello"), 2);
    replace_char(text, 'l', 'L');
    CLINGS_CHECK_STR(text, "heLLo");
    return clings_report();
}
