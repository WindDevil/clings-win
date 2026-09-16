/*
 * clings exercise: 08_arrays_strings/11_strcat_strncat
 * title: strcat and strncat
 * objective: Append a string while respecting the destination size.
 * hint: strncat appends at most n characters and always terminates.
 */

#include "clings/test.h"

#include <stddef.h>
#include <string.h>

int append_bounded(char *destination, size_t size, const char *source)
{
    size_t used = strlen(destination);
    if (used >= size) {
        return -1;
    }
    strncat(destination, source, size - used - 1);
    return 0;
}

int main(void)
{
    char buffer[16] = "Hello";
    char small[8] = "Hello";

    CLINGS_CHECK_INT(append_bounded(buffer, sizeof buffer, " C"), 0);
    CLINGS_CHECK_STR(buffer, "Hello C");
    CLINGS_CHECK_INT(append_bounded(small, sizeof small, " world"), 0);
    CLINGS_CHECK_STR(small, "Hello w");
    return clings_report();
}
