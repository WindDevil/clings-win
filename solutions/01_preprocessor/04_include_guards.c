/*
 * clings exercise: 01_preprocessor/04_include_guards
 * title: Include guards
 * objective: Prevent multiple inclusion with a preprocessor guard.
 * hint: Define the guard macro before the guarded declarations.
 */

#include "clings/test.h"

#ifndef CLINGS_GUARD_H
#define CLINGS_GUARD_H

int guarded_value(void);

#endif

int guarded_value(void)
{
    return 42;
}

int guard_is_defined(void)
{
#ifdef CLINGS_GUARD_H
    return 1;
#else
    return 0;
#endif
}

int main(void)
{
    CLINGS_CHECK_INT(guard_is_defined(), 1);
    CLINGS_CHECK_INT(guarded_value(), 42);
    return clings_report();
}
