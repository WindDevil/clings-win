/*
 * clings 练习: 07_pointers/01_pointer_basics
 * title: 解引用与取地址
 * objective: 通过指针读写数据。
 * hint: 只给参数本身赋值，不会改变调用方的变量。
 */

#include "clings/test.h"

int read_through(const int *value)
{
    return *value;
}

void write_through(int *value, int new_value)
{
    /* TODO: 通过指针写，不要只给本地参数赋值。 */
    value = &new_value;
}

int main(void)
{
    int value = 7;

    CLINGS_CHECK_INT(read_through(&value), 7);
    write_through(&value, 42);
    CLINGS_CHECK_INT(value, 42);
    return clings_report();
}
