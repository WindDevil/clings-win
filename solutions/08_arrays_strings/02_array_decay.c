/*
 * clings 练习: 08_arrays_strings/02_array_decay
 * title: 数组退化为指针
 * objective: 看清数组参数如何变成指针。
 * hint: 在函数内部，数组参数的类型是指针。
 */

#include "clings/test.h"

int local_array_length(void)
{
    int values[10];
    return (int)(sizeof(values) / sizeof(values[0]));
}

int parameter_is_pointer(const int *values)
{
    return sizeof(values) == sizeof(int *);
}

int main(void)
{
    int values[4] = {0};

    CLINGS_CHECK_INT(local_array_length(), 10);
    CLINGS_CHECK_INT(parameter_is_pointer(values), 1);
    return clings_report();
}
