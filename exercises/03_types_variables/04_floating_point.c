/*
 * clings exercise: 03_types_variables/04_floating_point
 * title: Floating-point comparison
 * objective: Compare floating-point values with an epsilon.
 * hint: Exact equality is usually the wrong comparison for computed doubles.
 */

#include "clings/test.h"

#include <math.h>

int nearly_equal(double a, double b, double epsilon)
{
    /* TODO: use an epsilon comparison. */
    return a == b;
}

int main(void)
{
    CLINGS_CHECK_INT(nearly_equal(0.1 + 0.2, 0.3, 1e-9), 1);
    CLINGS_CHECK_INT(nearly_equal(1.0, 1.1, 1e-9), 0);
    CLINGS_CHECK_INT(nearly_equal(-1.0, -1.0, 0.0), 1);
    return clings_report();
}
