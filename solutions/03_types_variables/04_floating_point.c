/*
 * clings 练习: 03_types_variables/04_floating_point
 * title: 浮点数比较
 * objective: 用 epsilon 比较浮点数。
 * hint: 对算出来的 double 做精确相等比较，通常都是错的。
 */

#include "clings/test.h"

#include <math.h>

int nearly_equal(double a, double b, double epsilon)
{
    return fabs(a - b) <= epsilon;
}

int main(void)
{
    CLINGS_CHECK_INT(nearly_equal(0.1 + 0.2, 0.3, 1e-9), 1);
    CLINGS_CHECK_INT(nearly_equal(1.0, 1.1, 1e-9), 0);
    CLINGS_CHECK_INT(nearly_equal(-1.0, -1.0, 0.0), 1);
    return clings_report();
}
