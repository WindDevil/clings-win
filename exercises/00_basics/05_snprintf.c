/*
 * clings exercise: 00_basics/05_snprintf
 * title: Safe formatting with snprintf
 * objective: Write formatted text into a fixed-size buffer.
 * hint: snprintf takes the buffer size and returns the number of characters it would write.
 */

#include "clings/test.h"

#include <stdio.h>

char buffer[32];

int format_greeting(void)
{
    /* TODO: format the greeting with the name C. */
    return snprintf(buffer, 32, "Hello, %s", "world");
}

int main(void)
{
    CLINGS_CHECK_INT(format_greeting(), 8);
    CLINGS_CHECK_STR(buffer, "Hello, C");
    return clings_report();
}
