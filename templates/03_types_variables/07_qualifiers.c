/*
 * clings 练习: 03_types_variables/07_qualifiers
 * title: 类型限定符与存储类说明符
 * objective: 使用 const、volatile、extern、auto 和 register。
 * hint: 限定符影响对象可以被怎样访问和优化。
 */

#include "clings/test.h"

extern int shared_value;
int shared_value = 42;

int const_value(void)
{
    const int value = 42;
    return value;
}

int volatile_value(void)
{
    /* TODO: 初始化这个 volatile 值。 */
    volatile int value = 0;
    return value;
}

int register_sum(void)
{
    register int sum = 0;
    for (register int i = 0; i < 3; ++i) {
        sum += i;
    }
    return sum;
}

int auto_value(void)
{
    auto int value = 5;
    return value;
}

int main(void)
{
    CLINGS_CHECK_INT(shared_value, 42);
    CLINGS_CHECK_INT(const_value(), 42);
    CLINGS_CHECK_INT(volatile_value(), 7);
    CLINGS_CHECK_INT(register_sum(), 3);
    CLINGS_CHECK_INT(auto_value(), 5);
    return clings_report();
}
