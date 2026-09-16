/*
 * clings 练习: 18_advanced_c/01_variadic
 * title: 变参函数
 * objective: 用 va_list 读取数量不定的 int 实参。
 * hint: 循环必须正好取出 count 个实参。
 */

#include "clings/test.h"

#include <stdarg.h>

long sum_variadic(int count, ...)
{
    va_list arguments;
    va_start(arguments, count);

    long sum = 0;
    /* TODO: 取出每一个可变实参。 */
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
