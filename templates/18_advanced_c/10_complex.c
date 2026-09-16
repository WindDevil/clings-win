/*
 * clings 练习: 18_advanced_c/10_complex
 * title: 复数
 * objective: 使用 double complex、I、conj、creal 和 cimag。
 * hint: conj 把虚部的符号取反。
 */

#include "clings/test.h"

#include <complex.h>

double complex make_complex(double real, double imaginary)
{
    return real + imaginary * I;
}

double complex conjugate_value(double complex value)
{
    /* TODO: 返回这个复数的共轭。 */
    return value;
}

double real_part(double complex value)
{
    return creal(value);
}

double imaginary_part(double complex value)
{
    return cimag(value);
}

int main(void)
{
    double complex value = make_complex(3.0, 4.0);
    double complex conjugated = conjugate_value(value);

    CLINGS_CHECK_INT(real_part(value) == 3.0, 1);
    CLINGS_CHECK_INT(imaginary_part(value) == 4.0, 1);
    CLINGS_CHECK_INT(imaginary_part(conjugated) == -4.0, 1);
    return clings_report();
}
