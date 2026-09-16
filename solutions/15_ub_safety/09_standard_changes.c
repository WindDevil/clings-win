/*
 * clings 练习: 15_ub_safety/09_standard_changes
 * title: C 标准的变化
 * objective: 在编译期判断 C 标准版本。
 * hint: C11 的 __STDC_VERSION__ 是 201112L，C17 是 201710L。
 */

#include "clings/test.h"

int c_standard_year(void)
{
    return (int)(__STDC_VERSION__ / 100L);
}

int has_c11(void)
{
#if defined(__STDC_VERSION__) && __STDC_VERSION__ >= 201112L
    return 1;
#else
    return 0;
#endif
}

int main(void)
{
    CLINGS_CHECK(c_standard_year() >= 2011);
    CLINGS_CHECK_INT(has_c11(), 1);
    return clings_report();
}
