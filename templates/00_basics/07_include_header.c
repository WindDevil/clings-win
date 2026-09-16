/*
 * clings exercise: 00_basics/07_include_header
 * title: Include the I/O header
 * objective: Include the standard header that declares printf.
 * hint: The compiler needs a declaration of printf; add the standard I/O header.
 */

#include "clings/test.h"

/* TODO: include the header that declares printf. */
int print_greeting(void)
{
    return printf("header works\n");
}

int main(void)
{
    CLINGS_CHECK_INT(print_greeting(), 13);
    return clings_report();
}
