/*
 * clings 练习: 06_functions/05_void_and_return
 * title: void 函数与 return 语句
 * objective: 在 void 函数里提前 return，在 int 函数里返回值。
 * hint: void 函数写 return; 就行；int 函数必须返回一个值。
 */

#include "clings/test.h"

static int global_value = 0;

void set_global_zero(void)
{
    global_value = 0;
}

int global_value_value(void)
{
    return global_value;
}

int early_return(int value)
{
    if (value < 0) {
        return -1;
    }
    /* TODO: 把非负的值翻倍。 */
    return value;
}

int main(void)
{
    set_global_zero();
    CLINGS_CHECK_INT(global_value_value(), 0);
    CLINGS_CHECK_INT(early_return(-3), -1);
    CLINGS_CHECK_INT(early_return(4), 8);
    return clings_report();
}
