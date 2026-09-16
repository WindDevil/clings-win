/*
 * clings exercise: 03_types_variables/10_octal_constants
 * title: Octal integer constants
 * objective: Recognize that a leading zero means base 8.
 * hint: 010 is 8, not 10; 0195 is not a valid C integer constant.
 */

#include "clings/test.h"

#include <stdlib.h>

int octal_constant(void)
{
    /* TODO: return the octal constant 010. */
    return 10;
}

int parse_c_integer(const char *text, int *out)
{
    char *end = NULL;
    long value = strtol(text, &end, 0);
    if (end == text || *end != '\0') {
        return -1;
    }
    *out = (int)value;
    return 0;
}

int main(void)
{
    int value = 0;

    CLINGS_CHECK_INT(octal_constant(), 8);
    CLINGS_CHECK_INT(parse_c_integer("010", &value), 0);
    CLINGS_CHECK_INT(value, 8);
    CLINGS_CHECK_INT(parse_c_integer("10", &value), 0);
    CLINGS_CHECK_INT(value, 10);
    CLINGS_CHECK_INT(parse_c_integer("0195", &value), -1);
    return clings_report();
}
