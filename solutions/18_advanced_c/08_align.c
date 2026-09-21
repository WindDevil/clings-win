/*
 * clings 练习: 18_advanced_c/08_align
 * title: alignof 与 alignas
 * objective: 查询对齐，并指定对齐。
 * hint: double 通常比 int 要求更严格的对齐。
 */

#include "clings/test.h"

#include <stdalign.h>

int align_of_int(void)
{
    return (int)alignof(int);
}

int align_of_double(void)
{
    return (int)alignof(double);
}

int main(void)
{
    CLINGS_CHECK(align_of_int() >= (int)alignof(short));
    CLINGS_CHECK(align_of_double() >= align_of_int());
    return clings_report();
}
