/*
 * clings 练习: 02_macros/04_variadic_macros
 * title: 变参宏
 * objective: 把可变实参列表转发给另一个变参函数。
 * hint: SUM(...) 要把每个实参都传下去，包括那个计数。
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
