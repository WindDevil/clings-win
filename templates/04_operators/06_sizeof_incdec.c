/*
 * clings 练习: 04_operators/06_sizeof_incdec
 * title: sizeof 与自增运算符
 * objective: 分清 sizeof 表达式与自增副作用。
 * hint: 后置自增返回旧值；前置自增返回新值。
 */

#include "clings/test.h"

int size_of_char(void)
{
    return (int)sizeof(char);
}

int post_increment(int *value)
{
    /* TODO: 这里用后置自增。 */
    return ++(*value);
}

int pre_increment(int *value)
{
    return ++(*value);
}

int main(void)
{
    int value = 5;

    CLINGS_CHECK_INT(size_of_char(), 1);
    CLINGS_CHECK_INT(post_increment(&value), 5);
    CLINGS_CHECK_INT(value, 6);
    CLINGS_CHECK_INT(pre_increment(&value), 7);
    CLINGS_CHECK_INT(value, 7);
    return clings_report();
}
