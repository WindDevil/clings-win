/*
 * clings 练习: 02_macros/09_macro_side_effects
 * title: 宏的副作用
 * objective: 看清函数式宏可能多次计算它的实参。
 * hint: NEXT_VALUE() 每出现一次，就把那个表达式展开一次。
 */

#include "clings/test.h"

static int calls = 0;

#define DOUBLE(x) ((x) + (x))

static int next_value(void)
{
    return ++calls;
}

int double_next(void)
{
    calls = 0;
    return DOUBLE(next_value());
}

int next_calls(void)
{
    return calls;
}

int main(void)
{
    CLINGS_CHECK_INT(double_next(), 3);
    CLINGS_CHECK_INT(next_calls(), 2);
    return clings_report();
}
