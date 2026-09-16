/*
 * clings 练习: 02_macros/11_macro_multiline
 * title: 多行宏
 * objective: 把宏定义续写到下一行。
 * hint: 行尾的反斜杠用来续写宏定义。
 */

#include "clings/test.h"

#define CLINGS_SUM(a, b, c) \
    ((a) + (b) + (c))

int sum_three(int a, int b, int c)
{
    return CLINGS_SUM(a, b, c);
}

int main(void)
{
    CLINGS_CHECK_INT(sum_three(1, 2, 3), 6);
    CLINGS_CHECK_INT(CLINGS_SUM(4, 5, 6), 15);
    return clings_report();
}
