/*
 * clings 练习: 02_macros/07_macro_not_typedef
 * title: 宏不是类型定义
 * objective: 指针类型用 typedef，不要用对象式宏。
 * hint: INT_POINTER a, b 会把 b 声明成 int，而不是 int *。
 */

#include "clings/test.h"

#include <stddef.h>

typedef int *int_pointer;
#define INT_POINTER int *

/* TODO: 两个声明都用这个 typedef。 */
INT_POINTER first = NULL, second = NULL;

int main(void)
{
    CLINGS_CHECK_INT((int)sizeof first, (int)sizeof(int *));
    CLINGS_CHECK_INT((int)sizeof second, (int)sizeof(int *));
    return clings_report();
}
