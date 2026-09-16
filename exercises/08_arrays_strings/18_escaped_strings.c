/*
 * clings 练习: 08_arrays_strings/18_escaped_strings
 * title: 转义字符串与续行
 * objective: 在字符串字面量里使用转义序列，并显式续行。
 * hint: 转义序列在字符串字面量里依然生效。
 */

#include "clings/test.h"

const char *escaped_text(void)
{
    /* TODO: 恢复这些转义序列。 */
    return "line1 line2 quoted";
}

int continued_sum(void)
{
    int sum = 1 + \
              2 + \
              3;
    return sum;
}

int comment_is_ignored(void)
{
    return 1 /* comment */ + 2;
}

int main(void)
{
    CLINGS_CHECK_STR(escaped_text(), "line1\nline2\t\"quoted\"");
    CLINGS_CHECK_INT(continued_sum(), 6);
    CLINGS_CHECK_INT(comment_is_ignored(), 3);
    return clings_report();
}
