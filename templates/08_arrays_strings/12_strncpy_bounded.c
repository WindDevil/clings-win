/*
 * clings exercise: 08_arrays_strings/12_strncpy_bounded
 * title: Bounded copying with strncpy
 * objective: Copy a string safely and always terminate the destination.
 * hint: strncpy does not guarantee a terminating NUL when the source is too long.
 */

#include "clings/test.h"

#include <stddef.h>
#include <string.h>

int copy_bounded(char *destination, size_t size, const char *source)
{
    if (size == 0) {
        return -1;
    }
    strncpy(destination, source, size - 1);
    /* TODO: terminate the copied string. */
    destination[size - 1] = 'x';
    return 0;
}

int main(void)
{
    char buffer[8];
    char small[4];

    CLINGS_CHECK_INT(copy_bounded(buffer, sizeof buffer, "hello"), 0);
    CLINGS_CHECK_STR(buffer, "hello");
    CLINGS_CHECK_INT(copy_bounded(small, sizeof small, "hello"), 0);
    CLINGS_CHECK_STR(small, "hel");
    CLINGS_CHECK_INT(copy_bounded(buffer, 0, "x"), -1);
    return clings_report();
}
