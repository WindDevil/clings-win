/*
 * clings exercise: 19_modern_c_library/02_tgmath
 * title: Type-generic math with tgmath.h
 * objective: Use sqrt with both double and float arguments through tgmath.h.
 * hint: tgmath.h selects the correct real function from the argument type.
 */

#include "clings/test.h"

#include <tgmath.h>

double generic_sqrt(double value)
{
    return sqrt(value);
}

float generic_sqrtf(float value)
{
    return sqrt(value);
}

int main(void)
{
    CLINGS_CHECK_INT(generic_sqrt(9.0) == 3.0, 1);
    CLINGS_CHECK_INT(generic_sqrtf(16.0f) == 4.0f, 1);
    return clings_report();
}
