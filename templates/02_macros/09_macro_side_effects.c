/*
 * clings exercise: 02_macros/09_macro_side_effects
 * title: Macro side effects
 * objective: See that a function-like macro can evaluate its argument more than once.
 * hint: NEXT_VALUE() expands to the expression every time it appears.
 */

#include "clings/test.h"

static int calls = 0;

/* TODO: expand the argument twice. */
#define DOUBLE(x) (x)

static int next_value(void)
{
    return ++calls;
}

int double_next(void)
{
    calls = 0;
    return DOUBLE(next_value());
}

int next_calls(void)
{
    return calls;
}

int main(void)
{
    CLINGS_CHECK_INT(double_next(), 3);
    CLINGS_CHECK_INT(next_calls(), 2);
    return clings_report();
}
