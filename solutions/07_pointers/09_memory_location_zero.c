/*
 * clings exercise: 07_pointers/09_memory_location_zero
 * title: Memory location zero
 * objective: Treat address zero as a null pointer, not as a valid object address.
 * hint: NULL is the portable null pointer constant.
 */

#include "clings/test.h"

#include <stddef.h>

int pointer_is_null(const void *pointer)
{
    return pointer == NULL;
}

int null_is_zero(void)
{
    return NULL == 0;
}

int main(void)
{
    int value = 1;

    CLINGS_CHECK_INT(pointer_is_null(NULL), 1);
    CLINGS_CHECK_INT(pointer_is_null(&value), 0);
    CLINGS_CHECK_INT(null_is_zero(), 1);
    return clings_report();
}
