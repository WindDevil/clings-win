/*
 * clings 练习: 07_pointers/12_pass_by_pointer
 * title: 值传递与指针传递
 * objective: 通过指针修改调用方的数据。
 * hint: 在覆盖 *a 之前先把它存下来。
 */

#include "clings/test.h"

void swap_int(int *a, int *b)
{
    /* TODO: 交换两个整数，并且不丢掉任何一个值。 */
    *a = *b;
    *b = *a;
}

void increment_all(int *values, int count)
{
    for (int i = 0; i < count; ++i) {
        ++values[i];
    }
}

int main(void)
{
    int a = 1;
    int b = 2;
    int values[] = {1, 2, 3};

    swap_int(&a, &b);
    CLINGS_CHECK_INT(a, 2);
    CLINGS_CHECK_INT(b, 1);
    increment_all(values, 3);
    CLINGS_CHECK_INT(values[0], 2);
    CLINGS_CHECK_INT(values[1], 3);
    CLINGS_CHECK_INT(values[2], 4);
    return clings_report();
}
