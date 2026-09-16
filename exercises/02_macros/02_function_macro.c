/*
 * clings 练习: 02_macros/02_function_macro
 * title: 函数式宏
 * objective: 用括号保护宏参数和整个展开结果。
 * hint: 参数和整个替换表达式都要加括号。
 */

#include "clings/test.h"

/* TODO: 给整个宏展开加括号。 */
#define MIN(a, b) (a) < (b) ? (a) : (b)
#define MAX(a, b) ((a) > (b) ? (a) : (b))

int min_value(int a, int b)
{
    return MIN(a, b);
}

int max_value(int a, int b)
{
    return MAX(a, b);
}

int main(void)
{
    CLINGS_CHECK_INT(min_value(3, 4), 3);
    CLINGS_CHECK_INT(max_value(3, 4), 4);
    CLINGS_CHECK_INT(MIN(2, 3) * 2, 4);
    return clings_report();
}
