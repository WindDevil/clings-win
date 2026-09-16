/*
 * clings exercise: 02_macros/01_object_macro
 * title: Object-like macros
 * objective: Use a named compile-time constant.
 * hint: Object-like macros are simple text substitutions.
 */

#include "clings/test.h"

#define CLINGS_BUFFER_SIZE 16
#define CLINGS_VERSION 2

int buffer_size(void)
{
    return CLINGS_BUFFER_SIZE;
}

int version(void)
{
    return CLINGS_VERSION;
}

int main(void)
{
    CLINGS_CHECK_INT(buffer_size(), 16);
    CLINGS_CHECK_INT(version(), 2);
    return clings_report();
}
