/*
 * clings exercise: 02_macros/02_function_macro
 * title: Function-like macros
 * objective: Protect macro arguments and the whole expansion with parentheses.
 * hint: Parenthesize both the parameters and the entire replacement expression.
 */

#include "clings/test.h"

/* TODO: parenthesize the whole macro expansion. */
#define MIN(a, b) (a) < (b) ? (a) : (b)
#define MAX(a, b) ((a) > (b) ? (a) : (b))

int min_value(int a, int b)
{
    return MIN(a, b);
}

int max_value(int a, int b)
{
    return MAX(a, b);
}

int main(void)
{
    CLINGS_CHECK_INT(min_value(3, 4), 3);
    CLINGS_CHECK_INT(max_value(3, 4), 4);
    CLINGS_CHECK_INT(MIN(2, 3) * 2, 4);
    return clings_report();
}
