/*
 * clings 练习: 02_macros/08_macro_not_typedef
 * title: 宏不是类型定义
 * objective: 指针类型用 typedef，不要用对象式宏。
 * hint: INT_POINTER a, b 会把 b 声明成 int，而不是 int *。
 */

#include "clings/test.h"

#include <stddef.h>

typedef int *int_pointer;
#define INT_POINTER int *

int_pointer first = NULL;
int_pointer second = NULL;

int main(void)
{
    CLINGS_CHECK_INT((int)sizeof first, (int)sizeof(int *));
    CLINGS_CHECK_INT((int)sizeof second, (int)sizeof(int *));
    return clings_report();
}
