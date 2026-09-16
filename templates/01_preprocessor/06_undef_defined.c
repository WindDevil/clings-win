/*
 * clings exercise: 01_preprocessor/06_undef_defined
 * title: #undef and defined
 * objective: Undefine a macro and test it with defined().
 * hint: #undef removes the macro before the second #if.
 */

#include "clings/test.h"

#define CLINGS_FEATURE 1

#if defined(CLINGS_FEATURE)
#define CLINGS_FEATURE_STATE 1
#else
#define CLINGS_FEATURE_STATE 0
#endif

/* TODO: remove CLINGS_FEATURE before the second test. */

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
