/*
 * clings exercise: 08_arrays_strings/13_sprintf_snprintf
 * title: sprintf and snprintf
 * objective: Format text with snprintf and understand truncation.
 * hint: snprintf returns the number of characters that would have been written.
 */

#include "clings/test.h"

#include <stdio.h>

int format_record(char *buffer, size_t size, const char *name, int age)
{
    /* TODO: format name followed by age. */
    return snprintf(buffer, size, "%d:%s", age, name);
}

int main(void)
{
    char buffer[32];
    char small[6];

    CLINGS_CHECK_INT(format_record(buffer, sizeof buffer, "Ada", 36), 6);
    CLINGS_CHECK_STR(buffer, "Ada:36");
    CLINGS_CHECK_INT(format_record(small, sizeof small, "Ada", 36), 6);
    CLINGS_CHECK_STR(small, "Ada:3");
    return clings_report();
}
