/*
 * clings 练习: 04_operators/03_short_circuit
 * title: 短路求值
 * objective: 观察 && 和 || 可能不计算右操作数。
 * hint: 只有左侧为真时，才会计算 && 的右侧。
 */

#include "clings/test.h"

static int side_effect_count = 0;

static int touch(void)
{
    ++side_effect_count;
    return 1;
}

int short_circuit_and(int left)
{
    /* TODO: 用逻辑与，不是按位与。 */
    return left & touch();
}

int short_circuit_or(int left)
{
    return left || touch();
}

int touch_count(void)
{
    return side_effect_count;
}

int main(void)
{
    CLINGS_CHECK_INT(short_circuit_and(0), 0);
    CLINGS_CHECK_INT(touch_count(), 0);
    CLINGS_CHECK_INT(short_circuit_or(1), 1);
    CLINGS_CHECK_INT(touch_count(), 0);
    CLINGS_CHECK_INT(short_circuit_and(1), 1);
    CLINGS_CHECK_INT(touch_count(), 1);
    return clings_report();
}
