/*
 * clings exercise: 03_types_variables/08_stdbool_stddef
 * title: stdbool.h and stddef.h
 * objective: Use bool and size_t from the standard headers.
 * hint: bool is defined in <stdbool.h>; size_t is defined in <stddef.h>.
 */

#include "clings/test.h"

#include <stdbool.h>
#include <stddef.h>

bool is_even(int value)
{
    return value % 2 == 0;
}

size_t size_of_int(void)
{
    return sizeof(int);
}

int main(void)
{
    CLINGS_CHECK_INT(is_even(4), 1);
    CLINGS_CHECK_INT(is_even(3), 0);
    CLINGS_CHECK_INT(size_of_int(), sizeof(int));
    return clings_report();
}
