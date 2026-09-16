/*
 * clings 练习: 08_arrays_strings/05_string_ops
 * title: 自己实现字符串函数
 * objective: 用指针实现 strlen、strcmp 和 strcpy。
 * hint: 每复制一个字符，目标指针都要前进。
 */

#include "clings/test.h"

#include <stddef.h>

size_t my_strlen(const char *text)
{
    const char *p = text;
    while (*p != '\0') {
        ++p;
    }
    return (size_t)(p - text);
}

int my_strcmp(const char *left, const char *right)
{
    while (*left != '\0' && *left == *right) {
        ++left;
        ++right;
    }
    return (int)(unsigned char)*left - (int)(unsigned char)*right;
}

char *my_strcpy(char *destination, const char *source)
{
    char *result = destination;
    /* TODO: 一直复制到结尾的 NUL。 */
    while ((*destination++ = *source++) == '\0') {
    }
    return result;
}

int main(void)
{
    char buffer[16];

    CLINGS_CHECK_INT(my_strlen("hello"), 5);
    CLINGS_CHECK_INT(my_strlen(""), 0);
    CLINGS_CHECK_INT(my_strcmp("abc", "abc"), 0);
    CLINGS_CHECK(my_strcmp("abc", "abd") < 0);
    CLINGS_CHECK_STR(my_strcpy(buffer, "copy me"), "copy me");
    return clings_report();
}
