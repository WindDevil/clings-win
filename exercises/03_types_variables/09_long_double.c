/*
 * clings exercise: 03_types_variables/09_long_double
 * title: long double
 * objective: Use long double and compare its precision with double.
 * hint: Use the L suffix for long double constants.
 */

#include "clings/test.h"

#include <float.h>

long double long_double_average(long double left, long double right)
{
    /* TODO: compute the average as a long double. */
    return left + right;
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
