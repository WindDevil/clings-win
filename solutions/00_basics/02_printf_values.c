/*
 * clings exercise: 00_basics/02_printf_values
 * title: Print a value
 * objective: Use printf with %d to print an integer value.
 * hint: Use %d for an int argument and include the newline in the format string.
 */

#include "clings/test.h"

#include <stdio.h>

int print_value(int value)
{
    return printf("%d\n", value);
}

int main(void)
{
    CLINGS_CHECK_INT(print_value(42), 3);
    return clings_report();
}
