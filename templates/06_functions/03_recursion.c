/*
 * clings 练习: 06_functions/03_recursion
 * title: 递归与基准情形
 * objective: 写出基准情形正确的递归函数。
 * hint: factorial(n) = n * factorial(n - 1)。
 */

#include "clings/test.h"

long factorial_recursive(int n)
{
    /* TODO: 乘以递归返回的结果。 */
    return n <= 1 ? 1 : n + factorial_recursive(n - 1);
}

int fibonacci(int n)
{
    return n <= 1 ? n : fibonacci(n - 1) + fibonacci(n - 2);
}

int main(void)
{
    CLINGS_CHECK_INT(factorial_recursive(0), 1);
    CLINGS_CHECK_INT(factorial_recursive(5), 120);
    CLINGS_CHECK_INT(fibonacci(0), 0);
    CLINGS_CHECK_INT(fibonacci(1), 1);
    CLINGS_CHECK_INT(fibonacci(8), 21);
    return clings_report();
}
