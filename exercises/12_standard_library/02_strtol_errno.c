/*
 * clings exercise: 12_standard_library/02_strtol_errno
 * title: Robust integer parsing
 * objective: Use strtol, errno, and the end pointer to validate input.
 * hint: Reject empty input, trailing characters, ERANGE, and out-of-range values.
 */

#include "clings/test.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>

int parse_int(const char *text, int *out)
{
    char *end = NULL;
    errno = 0;
    long value = strtol(text, &end, 10);

    /* TODO: validate every part of the conversion. */
    if (0) {
        return -1;
    }

    *out = (int)value;
    return 0;
}

int main(void)
{
    int out = 0;

    CLINGS_CHECK_INT(parse_int("123", &out), 0);
    CLINGS_CHECK_INT(out, 123);
    CLINGS_CHECK_INT(parse_int("-7", &out), 0);
    CLINGS_CHECK_INT(out, -7);
    CLINGS_CHECK_INT(parse_int("12x", &out), -1);
    CLINGS_CHECK_INT(parse_int("", &out), -1);
    CLINGS_CHECK_INT(parse_int("99999999999999999999", &out), -1);
    return clings_report();
}
