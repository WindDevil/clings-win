/*
 * clings 练习: 07_pointers/07_pointer_to_array
 * title: 数组指针与 &array
 * objective: 区分数组指针和指向首元素的指针。
 * hint: &a + 1 跨越整个数组，而不是一个元素。
 */

#include "clings/test.h"

#include <stddef.h>

int sum_row(const int (*row)[4])
{
    int sum = 0;
    for (int i = 0; i < 4; ++i) {
        sum += (*row)[i];
    }
    return sum;
}

int pointer_to_array_difference(void)
{
    int values[4] = {0};
    /* TODO: 一次跨越整个数组，不是一个元素。 */
    return (int)((char *)(values + 1) - (char *)values);
}

int main(void)
{
    const int row[4] = {1, 2, 3, 4};

    CLINGS_CHECK_INT(sum_row(&row), 10);
    CLINGS_CHECK_INT(pointer_to_array_difference(), (int)(sizeof(int) * 4));
    return clings_report();
}
