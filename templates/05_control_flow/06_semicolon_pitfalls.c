/*
 * clings 练习: 05_control_flow/06_semicolon_pitfalls
 * title: 分号与空语句陷阱
 * objective: 避免误用分号提前结束 if 或循环。
 * hint: if 后面直接写分号会产生一个空语句体。
 */

#include "clings/test.h"

int count_nonzero(const int *values, int count)
{
    int nonzero = 0;
    for (int i = 0; i < count; ++i) {
        if (values[i] != 0);
        {
            ++nonzero;
        }
    }
    return nonzero;
}

int main(void)
{
    const int values[] = {0, 1, 2};
    const int zeros[] = {0, 0, 0};

    CLINGS_CHECK_INT(count_nonzero(values, 3), 2);
    CLINGS_CHECK_INT(count_nonzero(zeros, 3), 0);
    return clings_report();
}
