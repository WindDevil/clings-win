/*
 * clings 练习: 18_advanced_c/05_generic
 * title: _Generic 选择
 * objective: 根据值的类型选择对应的表达式。
 * hint: 控制表达式不会被求值，只用到它的类型。
 */

#include "clings/test.h"

#define type_name(value)                                                     \
    _Generic((value), int: "int", double: "double", char *: "char *",        \
             default: "other")

int main(void)
{
    CLINGS_CHECK_STR(type_name(1), "int");
    CLINGS_CHECK_STR(type_name(1.0), "double");
    CLINGS_CHECK_STR(type_name("text"), "char *");
    CLINGS_CHECK_STR(type_name(1L), "other");
    return clings_report();
}
