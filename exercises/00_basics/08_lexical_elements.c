/*
 * clings 练习: 00_basics/08_lexical_elements
 * title: 注释与转义序列
 * objective: 正确使用注释和转义序列。
 * hint: 转义序列以反斜杠开头；注释需要成对的定界符。
 */

#include "clings/test.h"

char newline_character(void)
{
    /* TODO: 返回换行符。 */
    return 'n';
}

char tab_character(void)
{
    /* TODO: 返回制表符。 */
    return 't';
}

char backslash_character(void)
{
    /* TODO: 返回反斜杠字符。 */
    return '/';
}

int comment_is_ignored(void)
{
    /* TODO: 把注释闭合。 */
    return 1 /* comment + 2;
}

int main(void)
{
    CLINGS_CHECK_INT(newline_character(), '\n');
    CLINGS_CHECK_INT(tab_character(), '\t');
    CLINGS_CHECK_INT(backslash_character(), '\\');
    CLINGS_CHECK_INT(comment_is_ignored(), 3);
    return clings_report();
}
