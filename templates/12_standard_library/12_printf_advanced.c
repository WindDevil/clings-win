/*
 * clings exercise: 12_standard_library/12_printf_advanced
 * title: Advanced printf formatting
 * objective: Use width, zero padding, precision, and the * width argument.
 * hint: %08d zero-pads to width 8; %.3f uses three fractional digits.
 */

#include "clings/test.h"

#include <stdio.h>

int format_width(char *buffer, size_t size, int value)
{
    /* TODO: zero-pad the value to width 8. */
    return snprintf(buffer, size, "%d", value);
}

int format_precision(char *buffer, size_t size, double value)
{
    return snprintf(buffer, size, "%.3f", value);
}

int format_star(char *buffer, size_t size, int width, int value)
{
    return snprintf(buffer, size, "%*d", width, value);
}

int main(void)
{
    char buffer[32];

    CLINGS_CHECK_INT(format_width(buffer, sizeof buffer, 42), 8);
    CLINGS_CHECK_STR(buffer, "00000042");
    CLINGS_CHECK_INT(format_precision(buffer, sizeof buffer, 3.14159), 5);
    CLINGS_CHECK_STR(buffer, "3.142");
    CLINGS_CHECK_INT(format_star(buffer, sizeof buffer, 5, 42), 5);
    CLINGS_CHECK_STR(buffer, "   42");
    return clings_report();
}
