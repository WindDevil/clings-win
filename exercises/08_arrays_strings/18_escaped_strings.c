/*
 * clings exercise: 08_arrays_strings/18_escaped_strings
 * title: Escaped strings and line continuation
 * objective: Use escape sequences inside a string literal and continue lines explicitly.
 * hint: Escape sequences keep their meaning inside string literals.
 */

#include "clings/test.h"

const char *escaped_text(void)
{
    /* TODO: restore the escape sequences. */
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
