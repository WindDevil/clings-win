/*
 * clings 练习: 01_preprocessor/03_conditional_compilation
 * title: 条件编译
 * objective: 在预处理阶段按语言版本选择代码。
 * hint: C11 对应的 __STDC_VERSION__ 是 201112L。
 */

#include "clings/test.h"

#if defined(__STDC_VERSION__) && __STDC_VERSION__ >= 201112L
#define CLINGS_HAS_C11 1
#else
#define CLINGS_HAS_C11 0
#endif

int has_c11(void)
{
    return CLINGS_HAS_C11;
}

int main(void)
{
    CLINGS_CHECK_INT(has_c11(), 1);
    return clings_report();
}
