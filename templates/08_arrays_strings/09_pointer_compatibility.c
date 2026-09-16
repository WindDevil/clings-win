/*
 * clings 练习: 08_arrays_strings/09_pointer_compatibility
 * title: 指针兼容性与 const
 * objective: 通过指向 const 的指针传递非 const 数组。
 * hint: 指向 const 的指针可以指向非 const 数据。
 */

#include "clings/test.h"

#include <stddef.h>

int sum_const(const int *values, size_t count)
{
    int sum = 0;
    for (size_t i = 0; i < count; ++i) {
        sum += values[i];
    }
    return sum;
}

int pointer_compatibility(void)
{
    int values[3] = {1, 2, 3};
    const int *pointer = values;
    /* TODO: 把完整长度通过指向 const 的指针传出去。 */
    return sum_const(pointer, 2);
}

int main(void)
{
    const int const_values[3] = {4, 5, 6};

    CLINGS_CHECK_INT(pointer_compatibility(), 6);
    CLINGS_CHECK_INT(sum_const(const_values, 3), 15);
    return clings_report();
}
