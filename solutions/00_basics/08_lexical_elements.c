/*
 * clings exercise: 00_basics/08_lexical_elements
 * title: Comments and escape sequences
 * objective: Use comments and escape sequences correctly.
 * hint: Escape sequences start with a backslash; comments need both delimiters.
 */

#include "clings/test.h"

char newline_character(void)
{
    return '\n';
}

char tab_character(void)
{
    return '\t';
}

char backslash_character(void)
{
    return '\\';
}

int comment_is_ignored(void)
{
    return 1 /* comment */ + 2;
}

int main(void)
{
    CLINGS_CHECK_INT(newline_character(), '\n');
    CLINGS_CHECK_INT(tab_character(), '\t');
    CLINGS_CHECK_INT(backslash_character(), '\\');
    CLINGS_CHECK_INT(comment_is_ignored(), 3);
    return clings_report();
}
