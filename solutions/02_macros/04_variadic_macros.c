/*
 * clings exercise: 02_macros/04_variadic_macros
 * title: Variadic macros
 * objective: Forward a variable argument list to a variadic function.
 * hint: SUM(...) should pass every argument, including the count.
 */

#include "clings/test.h"

#include <stdarg.h>

int sum_variadic(int count, ...)
{
    va_list arguments;
    va_start(arguments, count);

    int sum = 0;
    for (int i = 0; i < count; ++i) {
        sum += va_arg(arguments, int);
    }

    va_end(arguments);
    return sum;
}

#define SUM(...) sum_variadic(__VA_ARGS__)

int main(void)
{
    CLINGS_CHECK_INT(SUM(3, 1, 2, 3), 6);
    CLINGS_CHECK_INT(SUM(0), 0);
    return clings_report();
}
