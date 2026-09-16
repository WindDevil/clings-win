/*
 * clings exercise: 00_basics/09_compiler_diagnostics
 * title: Read compiler diagnostics
 * objective: Fix a format-string warning that the compiler reports.
 * hint: Use %d to print an int; %s expects a string.
 */

#include "clings/test.h"

#include <stdio.h>

int print_number(int value)
{
    return printf("%d\n", value);
}

int main(void)
{
    CLINGS_CHECK_INT(print_number(42), 3);
    return clings_report();
}
