/*
 * clings 练习: 08_arrays_strings/10_asymmetric_bounds
 * title: 不对称边界
 * objective: 使用半开区间 [low, high)。
 * hint: 上界不包含在内：value < high。
 */

#include "clings/test.h"

int in_range(int value, int low, int high)
{
    /* TODO: 让上界不包含在内。 */
    return value >= low && value <= high;
}

int range_length(int low, int high)
{
    return high - low;
}

int loop_count(int low, int high)
{
    int count = 0;
    for (int value = low; value < high; ++value) {
        ++count;
    }
    return count;
}

int main(void)
{
    CLINGS_CHECK_INT(in_range(4, 0, 5), 1);
    CLINGS_CHECK_INT(in_range(5, 0, 5), 0);
    CLINGS_CHECK_INT(range_length(0, 5), 5);
    CLINGS_CHECK_INT(loop_count(0, 5), 5);
    return clings_report();
}
