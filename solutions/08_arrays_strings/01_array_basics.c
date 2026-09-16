/*
 * clings 练习: 08_arrays_strings/01_array_basics
 * title: 遍历数组
 * objective: 遍历数组，求出总和与最大值。
 * hint: 循环里要用 values[i]，不是 values[0]。
 */

#include "clings/test.h"

int array_sum(const int *values, int count)
{
    int sum = 0;
    for (int i = 0; i < count; ++i) {
        sum += values[i];
    }
    return sum;
}

int array_max(const int *values, int count)
{
    int maximum = values[0];
    for (int i = 1; i < count; ++i) {
        if (values[i] > maximum) {
            maximum = values[i];
        }
    }
    return maximum;
}

int main(void)
{
    const int values[] = {3, -1, 7, 2};

    CLINGS_CHECK_INT(array_sum(values, 4), 11);
    CLINGS_CHECK_INT(array_max(values, 4), 7);
    return clings_report();
}
