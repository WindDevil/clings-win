/*
 * clings 练习: 04_operators/08_assignment_vs_equality
 * title: 赋值与相等
 * objective: 比较用 ==，并认出 = 与 == 的陷阱。
 * hint: 单个 = 是赋值；两个 == 才是比较。
 */

#include "clings/test.h"

int is_equal(int left, int right)
{
    return left == right;
}

int compare_with_zero(int value)
{
    if (value == 0) {
        return 1;
    }
    return 0;
}

int main(void)
{
    CLINGS_CHECK_INT(is_equal(1, 1), 1);
    CLINGS_CHECK_INT(is_equal(1, 2), 0);
    CLINGS_CHECK_INT(compare_with_zero(0), 1);
    CLINGS_CHECK_INT(compare_with_zero(5), 0);
    return clings_report();
}
