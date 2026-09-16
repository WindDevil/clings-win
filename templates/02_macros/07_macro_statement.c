/*
 * clings exercise: 02_macros/07_macro_statement
 * title: Macros are not statements
 * objective: Use do { ... } while (0) for a statement-like macro.
 * hint: A bare block macro breaks if/else syntax.
 */

#include "clings/test.h"

/* TODO: make the macro behave like a single statement. */
#define SET_ZERO(pointer) { *(pointer) = 0; }

void set_if_positive(int *pointer, int condition)
{
    if (condition)
        SET_ZERO(pointer);
    else
        *pointer = 1;
}

int main(void)
{
    int value = 5;

    set_if_positive(&value, 1);
    CLINGS_CHECK_INT(value, 0);
    value = 5;
    set_if_positive(&value, 0);
    CLINGS_CHECK_INT(value, 1);
    return clings_report();
}
