/*
 * clings 练习: 15_ub_safety/01_signed_overflow
 * title: 避免有符号整数溢出
 * objective: 在做有符号加法之前检测溢出。
 * hint: 无符号运算会回绕；有符号溢出是未定义行为。
 */

#include "clings/test.h"

#include <limits.h>

int checked_add(int a, int b, int *out)
{
    if ((b > 0 && a > INT_MAX - b) || (b < 0 && a < INT_MIN - b)) {
        return -1;
    }
    *out = a + b;
    return 0;
}

int main(void)
{
    int out = 0;

    CLINGS_CHECK_INT(checked_add(INT_MAX, 1, &out), -1);
    CLINGS_CHECK_INT(checked_add(INT_MIN, -1, &out), -1);
    CLINGS_CHECK_INT(checked_add(20, 22, &out), 0);
    CLINGS_CHECK_INT(out, 42);
    return clings_report();
}
