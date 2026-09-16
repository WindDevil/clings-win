/*
 * clings exercise: 08_arrays_strings/15_strtod
 * title: Converting strings to double
 * objective: Parse a double with strtod and reject trailing input.
 * hint: Check errno, endptr, and the character after the number.
 */

#include "clings/test.h"

#include <errno.h>
#include <stdlib.h>

int parse_double(const char *text, double *out)
{
    char *end = NULL;
    errno = 0;
    double value = strtod(text, &end);
    /* TODO: reject trailing characters. */
    if (errno == ERANGE || end == text) {
        return -1;
    }
    *out = value;
    return 0;
}

int main(void)
{
    double value = 0.0;

    CLINGS_CHECK_INT(parse_double("3.14", &value), 0);
    CLINGS_CHECK_INT(value == 3.14, 1);
    CLINGS_CHECK_INT(parse_double("3.14x", &value), -1);
    CLINGS_CHECK_INT(parse_double("", &value), -1);
    return clings_report();
}
