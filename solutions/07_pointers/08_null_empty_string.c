/*
 * clings 练习: 07_pointers/08_null_empty_string
 * title: NULL、空串与 NUL
 * objective: 区分空指针、空串和 NUL 字符。
 * hint: NULL 是空指针；"" 是合法的空串；'\0' 是 NUL 字符。
 */

#include "clings/test.h"

#include <stddef.h>
#include <string.h>

int length_or_zero(const char *text)
{
    return text == NULL ? 0 : (int)strlen(text);
}

int is_empty_string(const char *text)
{
    return text != NULL && text[0] == '\0';
}

int main(void)
{
    CLINGS_CHECK_INT(length_or_zero(NULL), 0);
    CLINGS_CHECK_INT(length_or_zero(""), 0);
    CLINGS_CHECK_INT(is_empty_string(""), 1);
    CLINGS_CHECK_INT(is_empty_string(NULL), 0);
    return clings_report();
}
