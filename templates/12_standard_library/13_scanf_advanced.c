/*
 * clings exercise: 12_standard_library/13_scanf_advanced
 * title: Advanced scanf input
 * objective: Use field width and a scanset in sscanf.
 * hint: %3d reads at most three digits; %[abc] reads only a, b, and c.
 */

#include "clings/test.h"

#include <stdio.h>

int parse_field(const char *input, int *out)
{
    /* TODO: read at most three digits. */
    return sscanf(input, "%d", out) == 1 ? 0 : -1;
}

int parse_set(const char *input, char *out, size_t size)
{
    if (size == 0) {
        return -1;
    }
    out[0] = '\0';
    return sscanf(input, "%[abc]", out) == 1 ? 0 : -1;
}

int main(void)
{
    int value = 0;
    char buffer[16];

    CLINGS_CHECK_INT(parse_field("12345", &value), 0);
    CLINGS_CHECK_INT(value, 123);
    CLINGS_CHECK_INT(parse_set("abcxyz", buffer, sizeof buffer), 0);
    CLINGS_CHECK_STR(buffer, "abc");
    CLINGS_CHECK_INT(parse_set("xyz", buffer, sizeof buffer), -1);
    return clings_report();
}
