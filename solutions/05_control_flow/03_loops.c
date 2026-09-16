/*
 * clings exercise: 05_control_flow/03_loops
 * title: for and while loops
 * objective: Get loop bounds and accumulators right.
 * hint: sum_to(n) includes n; factorial multiplies 2 through n.
 */

#include "clings/test.h"

long sum_to(int n)
{
    long sum = 0;
    for (int i = 1; i <= n; ++i) {
        sum += i;
    }
    return sum;
}

long factorial(int n)
{
    long result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

int main(void)
{
    CLINGS_CHECK_INT(sum_to(0), 0);
    CLINGS_CHECK_INT(sum_to(5), 15);
    CLINGS_CHECK_INT(factorial(0), 1);
    CLINGS_CHECK_INT(factorial(5), 120);
    return clings_report();
}
