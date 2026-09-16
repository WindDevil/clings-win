/*
 * clings 练习: 04_operators/07_compound_assignment
 * title: 复合赋值与逗号运算符
 * objective: 使用 +=、-=、*=、/=、%= 和逗号运算符。
 * hint: 逗号运算符从左到右求值，结果是右操作数。
 */

#include "clings/test.h"

int compound_demo(int value)
{
    value += 3;
    value *= 2;
    value -= 1;
    value /= 2;
    value %= 5;
    return value;
}

int comma_sum(int left, int right)
{
    int sum = 0;
    sum = (left++, right++, left + right);
    return sum;
}

int main(void)
{
    CLINGS_CHECK_INT(compound_demo(1), 3);
    CLINGS_CHECK_INT(comma_sum(2, 3), 7);
    return clings_report();
}
