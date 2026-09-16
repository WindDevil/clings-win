/*
 * clings exercise: 04_operators/02_precedence
 * title: Precedence and parentheses
 * objective: Use parentheses to express intent clearly.
 * hint: Multiplication binds more tightly than addition.
 */

#include "clings/test.h"

int precedence_demo(int a, int b, int c)
{
    return a + b * c;
}

int parenthesized(int a, int b, int c)
{
    return (a + b) * c;
}

int main(void)
{
    CLINGS_CHECK_INT(precedence_demo(2, 3, 4), 14);
    CLINGS_CHECK_INT(parenthesized(2, 3, 4), 20);
    CLINGS_CHECK_INT(parenthesized(1, 1, 0), 0);
    return clings_report();
}
