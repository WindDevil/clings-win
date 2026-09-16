/*
 * clings 练习: 03_types_variables/09_long_double
 * title: long double
 * objective: 使用 long double，并与 double 比较精度。
 * hint: long double 常量要加 L 后缀。
 */

#include "clings/test.h"

#include <float.h>

long double long_double_average(long double left, long double right)
{
    return (left + right) / 2.0L;
}

int long_double_has_extra_precision(void)
{
    return LDBL_DIG >= DBL_DIG ? 1 : 0;
}

int main(void)
{
    CLINGS_CHECK_INT(long_double_average(1.5L, 2.5L) == 2.0L, 1);
    CLINGS_CHECK_INT(long_double_has_extra_precision(), 1);
    return clings_report();
}
