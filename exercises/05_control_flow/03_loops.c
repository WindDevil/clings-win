/*
 * clings 练习: 05_control_flow/03_loops
 * title: for 与 while 循环
 * objective: 把循环边界和累加器写对。
 * hint: sum_to(n) 把 n 也算进去；factorial 相乘的范围是 2 到 n。
 */

#include "clings/test.h"

long sum_to(int n)
{
    long sum = 0;
    /* TODO: 求和时把 n 也算进去。 */
    for (int i = 1; i < n; ++i) {
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
