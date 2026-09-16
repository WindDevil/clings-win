/*
 * clings exercise: 02_macros/08_macro_not_typedef
 * title: Macros are not type definitions
 * objective: Use typedef instead of an object-like macro for pointer types.
 * hint: INT_POINTER a, b declares b as int, not int *.
 */

#include "clings/test.h"

#include <stddef.h>

typedef int *int_pointer;
#define INT_POINTER int *

/* TODO: use the typedef for both declarations. */
INT_POINTER first = NULL, second = NULL;

int main(void)
{
    CLINGS_CHECK_INT((int)sizeof first, (int)sizeof(int *));
    CLINGS_CHECK_INT((int)sizeof second, (int)sizeof(int *));
    return clings_report();
}
