/*
 * clings 练习: 15_ub_safety/05_sequence_points
 * title: 序列点
 * objective: 避免对同一对象做无序列点保护的读写。
 * hint: 先读出旧值，再更新对象，最后返回旧值。
 */

#include "clings/test.h"

int next_value(int *value)
{
    int current = *value;
    *value = current + 1;
    return current;
}

int main(void)
{
    int value = 5;

    CLINGS_CHECK_INT(next_value(&value), 5);
    CLINGS_CHECK_INT(value, 6);
    CLINGS_CHECK_INT(next_value(&value), 6);
    CLINGS_CHECK_INT(value, 7);
    return clings_report();
}
