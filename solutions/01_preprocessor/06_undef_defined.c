/*
 * clings 练习: 01_preprocessor/06_undef_defined
 * title: #undef 与 defined
 * objective: 取消宏定义，并用 defined() 测试它。
 * hint: #undef 会在第二个 #if 之前撤销这个宏。
 */

#include "clings/test.h"

#define CLINGS_FEATURE 1

#if defined(CLINGS_FEATURE)
#define CLINGS_FEATURE_STATE 1
#else
#define CLINGS_FEATURE_STATE 0
#endif

#undef CLINGS_FEATURE

#ifdef CLINGS_FEATURE
#define CLINGS_AFTER_UNDEF 1
#else
#define CLINGS_AFTER_UNDEF 0
#endif

int feature_state(void)
{
    return CLINGS_FEATURE_STATE;
}

int after_undef(void)
{
    return CLINGS_AFTER_UNDEF;
}

int main(void)
{
    CLINGS_CHECK_INT(feature_state(), 1);
    CLINGS_CHECK_INT(after_undef(), 0);
    return clings_report();
}
