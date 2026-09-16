/*
 * clings 练习: 02_macros/07_macro_statement
 * title: 宏不是语句
 * objective: 用 do { ... } while (0) 写像语句一样的宏。
 * hint: 光秃秃的块状宏会破坏 if/else 的语法。
 */

#include "clings/test.h"

#define SET_ZERO(pointer) do { *(pointer) = 0; } while (0)

void set_if_positive(int *pointer, int condition)
{
    if (condition)
        SET_ZERO(pointer);
    else
        *pointer = 1;
}

int main(void)
{
    int value = 5;

    set_if_positive(&value, 1);
    CLINGS_CHECK_INT(value, 0);
    value = 5;
    set_if_positive(&value, 0);
    CLINGS_CHECK_INT(value, 1);
    return clings_report();
}
