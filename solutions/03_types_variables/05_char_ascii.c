/*
 * clings exercise: 03_types_variables/05_char_ascii
 * title: Characters and ASCII
 * objective: Work with char values and the ctype classification functions.
 * hint: Lowercase letters live in a contiguous range only for the execution character set.
 */

#include "clings/test.h"

#include <ctype.h>

int is_ascii_digit(char c)
{
    return c >= '0' && c <= '9';
}

char to_upper_ascii(char c)
{
    return (c >= 'a' && c <= 'z') ? (char)(c - 'a' + 'A') : c;
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
