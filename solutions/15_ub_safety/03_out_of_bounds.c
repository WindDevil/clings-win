/*
 * clings 练习: 15_ub_safety/03_out_of_bounds
 * title: 边界检查
 * objective: 拒绝超出逻辑长度的下标。
 * hint: 下标小于 0，或大于等于 count，就是无效的。
 */

#include "clings/test.h"

int get_or_default(const int *values, int count, int index, int fallback)
{
    if (index < 0 || index >= count) {
        return fallback;
    }
    return values[index];
}

int main(void)
{
    const int values[] = {10, 20, 30, 999};

    CLINGS_CHECK_INT(get_or_default(values, 3, 0, 123), 10);
    CLINGS_CHECK_INT(get_or_default(values, 3, 2, 123), 30);
    CLINGS_CHECK_INT(get_or_default(values, 3, 3, 123), 123);
    CLINGS_CHECK_INT(get_or_default(values, 3, -1, 123), 123);
    return clings_report();
}
