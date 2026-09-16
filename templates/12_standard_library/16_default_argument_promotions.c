/*
 * clings 练习: 12_standard_library/16_default_argument_promotions
 * title: 默认实参提升
 * objective: 使用变参函数期望的提升后类型。
 * hint: char 和 short 提升为 int；float 提升为 double。
 */

#include "clings/test.h"

#include <stdarg.h>

int sum_promoted(int count, ...)
{
    va_list arguments;
    va_start(arguments, count);
    int sum = 0;
    for (int i = 0; i < count; ++i) {
        /* TODO: 取出提升为 int 的那个实参。 */
        sum += 1;
    }
    va_end(arguments);
    return sum;
}

double sum_double_promoted(int count, ...)
{
    va_list arguments;
    va_start(arguments, count);
    double sum = 0.0;
    for (int i = 0; i < count; ++i) {
        sum += va_arg(arguments, double);
    }
    va_end(arguments);
    return sum;
}

int main(void)
{
    CLINGS_CHECK_INT(sum_promoted(3, (char)1, (short)2, 3), 6);
    CLINGS_CHECK_INT(sum_double_promoted(2, 1.5f, 2.5f) == 4.0, 1);
    return clings_report();
}
