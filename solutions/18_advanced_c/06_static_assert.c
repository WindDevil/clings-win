/*
 * clings exercise: 18_advanced_c/06_static_assert
 * title: Compile-time assertions
 * objective: Use _Static_assert to enforce assumptions at compile time.
 * hint: A failed static assertion must make the build fail.
 */

#include "clings/test.h"

#include <limits.h>

_Static_assert(sizeof(int) >= 2, "int must be at least 16 bits");
_Static_assert(CHAR_BIT == 8, "this course assumes 8-bit bytes");

int static_asserts_passed(void)
{
    return 1;
}

int main(void)
{
    CLINGS_CHECK_INT(static_asserts_passed(), 1);
    return clings_report();
}
