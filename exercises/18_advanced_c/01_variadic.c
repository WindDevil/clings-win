/*
 * clings exercise: 18_advanced_c/01_variadic
 * title: Variadic functions
 * objective: Read a variable number of int arguments with va_list.
 * hint: The loop must consume exactly count arguments.
 */

#include "clings/test.h"

#include <stdarg.h>

long sum_variadic(int count, ...)
{
    va_list arguments;
    va_start(arguments, count);

    long sum = 0;
    /* TODO: consume every variadic argument. */
    for (int i = 0; i < count - 1; ++i) {
        sum += va_arg(arguments, int);
    }

    va_end(arguments);
    return sum;
}

int main(void)
{
    CLINGS_CHECK_INT(sum_variadic(0), 0);
    CLINGS_CHECK_INT(sum_variadic(3, 1, 2, 3), 6);
    CLINGS_CHECK_INT(sum_variadic(5, 10, 20, 30, 40, 50), 150);
    return clings_report();
}
