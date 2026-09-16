/*
 * clings 练习: 02_macros/06_macro_whitespace
 * title: 宏定义里的空白
 * objective: 记住一个空格就能把函数式宏变成对象式宏。
 * hint: 左括号必须紧跟宏名。
 */

#include "clings/test.h"

#define SQUARE(value) ((value) * (value))

int square_value(int value)
{
    return SQUARE(value);
}

int main(void)
{
    CLINGS_CHECK_INT(square_value(4), 16);
    CLINGS_CHECK_INT(SQUARE(3), 9);
    return clings_report();
}
