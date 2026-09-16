/*
 * clings exercise: 12_standard_library/14_ctype_full
 * title: ctype.h classification and conversion
 * objective: Use isalnum and toupper with unsigned char casts.
 * hint: Pass (unsigned char) to ctype functions to avoid negative arguments.
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
