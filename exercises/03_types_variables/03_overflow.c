/*
 * clings 练习: 03_types_variables/03_overflow
 * title: 无符号回绕与带检查的有符号加法
 * objective: 理解取模回绕，并避开有符号整数溢出。
 * hint: 在 a 上加 b 之前，先检查 INT_MAX - b。
 */

#include "clings/test.h"

#include <limits.h>

unsigned wrap_add(unsigned a, unsigned b)
{
    return a + b;
}

int add_overflows(int a, int b)
{
    /* TODO: 做加法之前先检测溢出。 */
    return 0;
}

long add_wide(int a, int b)
{
    return (long)a + (long)b;
}

int main(void)
{
    CLINGS_CHECK_INT(wrap_add(UINT_MAX, 1u), 0);
    CLINGS_CHECK_INT(add_overflows(INT_MAX, 1), 1);
    CLINGS_CHECK_INT(add_overflows(INT_MIN, -1), 1);
    CLINGS_CHECK_INT(add_overflows(2, 3), 0);
    CLINGS_CHECK_INT(add_wide(2, 3), 5);
    return clings_report();
}
