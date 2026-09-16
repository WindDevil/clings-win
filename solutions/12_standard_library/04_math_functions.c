/*
 * clings 练习: 12_standard_library/04_math_functions
 * title: 数学库
 * objective: 使用 math.h 里的 hypot 等函数。
 * hint: hypot(x, y) 计算 sqrt(x*x + y*y)，并避免本可避免的溢出。
 */

#include "clings/test.h"

#include <math.h>

double distance(double x1, double y1, double x2, double y2)
{
    return hypot(x2 - x1, y2 - y1);
}

int main(void)
{
    CLINGS_CHECK_INT(distance(0.0, 0.0, 3.0, 4.0) == 5.0, 1);
    CLINGS_CHECK_INT(distance(1.0, 1.0, 1.0, 1.0) == 0.0, 1);
    return clings_report();
}
