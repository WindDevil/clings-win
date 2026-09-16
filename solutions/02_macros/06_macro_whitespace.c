/*
 * clings exercise: 02_macros/06_macro_whitespace
 * title: Whitespace in macro definitions
 * objective: Remember that a space can turn a function-like macro into an object-like macro.
 * hint: The ( must immediately follow the macro name.
 */

#include "clings/test.h"

#define SQUARE(value) ((value) * (value))

int square_value(int value)
{
    return SQUARE(value);
}

int main(void)
{
    CLINGS_CHECK_INT(square_value(4), 16);
    CLINGS_CHECK_INT(SQUARE(3), 9);
    return clings_report();
}
