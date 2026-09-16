/*
 * clings exercise: 06_functions/05_void_and_return
 * title: void functions and return statements
 * objective: Return early from a void function and return values from int functions.
 * hint: A void function uses a bare return; an int function must return a value.
 */

#include "clings/test.h"

static int global_value = 0;

void set_global_zero(void)
{
    global_value = 0;
}

int global_value_value(void)
{
    return global_value;
}

int early_return(int value)
{
    if (value < 0) {
        return -1;
    }
    return value * 2;
}

int main(void)
{
    set_global_zero();
    CLINGS_CHECK_INT(global_value_value(), 0);
    CLINGS_CHECK_INT(early_return(-3), -1);
    CLINGS_CHECK_INT(early_return(4), 8);
    return clings_report();
}
