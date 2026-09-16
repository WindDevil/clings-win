/*
 * clings 练习: 19_modern_c_library/02_tgmath
 * title: 用 tgmath.h 做类型通用数学运算
 * objective: 通过 tgmath.h 用 sqrt 处理 double 和 float 实参。
 * hint: tgmath.h 会根据实参类型挑出正确的实数函数。
 */

#include "clings/test.h"

#include <tgmath.h>

double generic_sqrt(double value)
{
    return sqrt(value);
}

float generic_sqrtf(float value)
{
    /* TODO: 用类型通用的 sqrt。 */
    return value;
}

int main(void)
{
    CLINGS_CHECK_INT(generic_sqrt(9.0) == 3.0, 1);
    CLINGS_CHECK_INT(generic_sqrtf(16.0f) == 4.0f, 1);
    return clings_report();
}
