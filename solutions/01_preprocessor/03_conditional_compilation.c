/*
 * clings exercise: 01_preprocessor/03_conditional_compilation
 * title: Conditional compilation
 * objective: Select code at preprocessing time based on the language version.
 * hint: C11 introduced __STDC_VERSION__ value 201112L.
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
