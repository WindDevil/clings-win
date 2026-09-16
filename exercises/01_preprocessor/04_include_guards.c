/*
 * clings 练习: 01_preprocessor/04_include_guards
 * title: 头文件保护
 * objective: 用预处理保护防止重复引入。
 * hint: 保护宏要定义在被保护的声明之前。
 */

#include "clings/test.h"

#ifndef CLINGS_GUARD_H
/* TODO: 定义头文件保护宏。 */

int guarded_value(void);

#endif

int guarded_value(void)
{
    return 42;
}

int guard_is_defined(void)
{
#ifdef CLINGS_GUARD_H
    return 1;
#else
    return 0;
#endif
}

int main(void)
{
    CLINGS_CHECK_INT(guard_is_defined(), 1);
    CLINGS_CHECK_INT(guarded_value(), 42);
    return clings_report();
}
