/*
 * clings exercise: 18_advanced_c/05_generic
 * title: _Generic selection
 * objective: Choose an expression based on the type of a value.
 * hint: The controlling expression is not evaluated; only its type is used.
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
