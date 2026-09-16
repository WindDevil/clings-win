/*
 * clings 练习: 02_macros/10_assert_macro
 * title: 断言与防御式编程
 * objective: 程序员错误用 assert，用户错误用返回值。
 * hint: 分母为零属于正常的错误，返回 -1，不要真的去除。
 */

#include "clings/test.h"

#include <assert.h>
#include <stddef.h>

int checked_divide(int numerator, int denominator, int *out)
{
    assert(out != NULL);
    if (denominator == 0) {
        /* TODO: 报告这个错误。 */
        return 0;
    }
    *out = numerator / denominator;
    return 0;
}

int main(void)
{
    int out = 0;

    CLINGS_CHECK_INT(checked_divide(10, 2, &out), 0);
    CLINGS_CHECK_INT(out, 5);
    CLINGS_CHECK_INT(checked_divide(10, 0, &out), -1);
    return clings_report();
}
