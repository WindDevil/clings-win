/*
 * clings exercise: 01_preprocessor/01_include_standard
 * title: #include with a standard header
 * objective: Include the standard header that declares fixed-width integer types.
 * hint: Add the standard header that declares int32_t and INT32_MAX.
 */

#include "clings/test.h"

#include <stdint.h>

int32_t largest_int32(void)
{
    return INT32_MAX;
}

int main(void)
{
    CLINGS_CHECK_INT(largest_int32(), INT32_MAX);
    return clings_report();
}
