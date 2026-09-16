/*
 * clings exercise: 13_character_io/05_getchar_putchar
 * title: getchar and putchar
 * objective: Use the standard input/output character macros directly.
 * hint: ungetc can push a character back onto stdin for a test.
 */

#include "clings/test.h"

#include <stdio.h>

int read_one_character(void)
{
    return getchar();
}

int write_one_character(int character)
{
    return putchar(character);
}

int main(void)
{
    CLINGS_CHECK_INT(ungetc('x', stdin), 'x');
    CLINGS_CHECK_INT(read_one_character(), 'x');
    CLINGS_CHECK_INT(write_one_character('y'), 'y');
    return clings_report();
}
