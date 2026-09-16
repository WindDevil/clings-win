/*
 * clings 练习: 18_advanced_c/02_setjmp_longjmp
 * title: setjmp 与 longjmp
 * objective: 用非局部跳转实现一条简单的错误路径。
 * hint: longjmp 会把控制权交回与它配对的 setjmp 调用处。
 */

#include "clings/test.h"

#include <setjmp.h>

static jmp_buf jump_buffer;

static int checked_positive(int value)
{
    if (value < 0) {
        longjmp(jump_buffer, 1);
    }
    return value;
}

int run_checked(int value, int *out)
{
    if (setjmp(jump_buffer) != 0) {
        return -1;
    }
    *out = checked_positive(value);
    return 0;
}

int main(void)
{
    int out = 0;

    CLINGS_CHECK_INT(run_checked(5, &out), 0);
    CLINGS_CHECK_INT(out, 5);
    CLINGS_CHECK_INT(run_checked(-1, &out), -1);
    return clings_report();
}
