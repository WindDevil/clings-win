/*
 * clings 练习: 05_control_flow/01_if_else
 * title: if 与 else
 * objective: 写出清晰的条件分支。
 * hint: 先判断正数，再判断负数，最后处理剩下的零。
 */

#include "clings/test.h"

int sign_of(int value)
{
    if (value > 0) {
        return 1;
    }
    if (value < 0) {
        return -1;
    }
    return 0;
}

int max_of(int a, int b)
{
    return (a > b) ? a : b;
}

int main(void)
{
    CLINGS_CHECK_INT(sign_of(42), 1);
    CLINGS_CHECK_INT(sign_of(-7), -1);
    CLINGS_CHECK_INT(sign_of(0), 0);
    CLINGS_CHECK_INT(max_of(3, 9), 9);
    CLINGS_CHECK_INT(max_of(-1, -2), -1);
    return clings_report();
}
