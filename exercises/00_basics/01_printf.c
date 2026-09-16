/*
 * clings exercise: 00_basics/01_printf
 * title: Print with printf
 * objective: Use printf to print a line of text.
 * hint: printf returns the number of characters printed, including the newline.
 */

#include "clings/test.h"

#include <stdio.h>

int print_greeting(void)
{
    /* TODO: print Hello, C! followed by a newline. */
    return printf("Hello, world!\n");
}

int main(void)
{
    CLINGS_CHECK_INT(print_greeting(), 10);
    return clings_report();
}
