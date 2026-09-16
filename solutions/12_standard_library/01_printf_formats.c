/*
 * clings exercise: 12_standard_library/01_printf_formats
 * title: printf format specifiers
 * objective: Match each conversion specifier to its argument type.
 * hint: long values use %ld; doubles use %f or %.2f.
 */

#include "clings/test.h"

#include <stdio.h>

int format_all(char *buffer, size_t size, long value, double real,
               const char *text)
{
    return snprintf(buffer, size, "%ld %.2f %s", value, real, text);
}

int main(void)
{
    char buffer[64];

    CLINGS_CHECK_INT(format_all(buffer, sizeof buffer, 42L, 3.5, "ok"), 10);
    CLINGS_CHECK_STR(buffer, "42 3.50 ok");
    return clings_report();
}
