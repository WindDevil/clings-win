/*
 * clings 练习: 04_operators/01_arithmetic
 * title: 整数运算
 * objective: 练习整数除法、取模和截断。
 * hint: 整数除法向零截断。
 */

#include "clings/test.h"

int quotient(int a, int b)
{
    return a / b;
}

int int_remainder(int a, int b)
{
    /* TODO: 返回余数，不是商。 */
    return a / b;
}

int average_floor(int a, int b)
{
    return (a + b) / 2;
}

int main(void)
{
    CLINGS_CHECK_INT(quotient(7, 3), 2);
    CLINGS_CHECK_INT(quotient(-7, 3), -2);
    CLINGS_CHECK_INT(int_remainder(7, 3), 1);
    CLINGS_CHECK_INT(average_floor(2, 3), 2);
    return clings_report();
}
