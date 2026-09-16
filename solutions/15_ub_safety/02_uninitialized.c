/*
 * clings 练习: 15_ub_safety/02_uninitialized
 * title: 先初始化再使用
 * objective: 让每个局部变量都有确定的初值。
 * hint: 把 result 初值设为 -1，兜底路径才有确定行为。
 */

#include "clings/test.h"

int initialized_or_default(int value)
{
    int result = -1;
    if (value > 0) {
        result = value;
    }
    return result;
}

int main(void)
{
    CLINGS_CHECK_INT(initialized_or_default(0), -1);
    CLINGS_CHECK_INT(initialized_or_default(-5), -1);
    CLINGS_CHECK_INT(initialized_or_default(7), 7);
    return clings_report();
}
