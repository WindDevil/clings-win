/*
 * clings 练习: 07_pointers/10_one_past_pointer
 * title: 越尾一个位置的指针运算
 * objective: 不要把单个对象的指针当成数组用。
 * hint: 对单个对象来说，只有越尾一个位置的那个指针是合法的，而且不能解引用。
 */

#include "clings/test.h"

int one_past_offset(void)
{
    int value = 42;
    int *pointer = &value;
    int *one_past = pointer + 1;
    /* TODO: 对单个对象来说，只有越尾一个位置是合法的。 */
    return (int)(one_past - pointer + 1);
}

int single_object_value(void)
{
    int value = 42;
    int *pointer = &value;
    return *pointer;
}

int main(void)
{
    CLINGS_CHECK_INT(one_past_offset(), 1);
    CLINGS_CHECK_INT(single_object_value(), 42);
    return clings_report();
}
