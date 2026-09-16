/*
 * clings exercise: 09_dynamic_memory/05_buffer_bounds
 * title: Respecting buffer bounds
 * objective: Copy at most dest_size - 1 bytes and always terminate.
 * hint: Leave room for the terminating NUL.
 */

#include "clings/test.h"

#include <stddef.h>

int bounded_copy(char *destination, size_t destination_size, const char *source)
{
    size_t i = 0;
    /* TODO: leave room for the terminator. */
    for (; i < destination_size && source[i] != '\0'; ++i) {
        destination[i] = source[i];
    }
    destination[i] = '\0';
    return (int)i;
}

int main(void)
{
    char buffer[5];
    int copied = 0;

    buffer[4] = 'X';
    copied = bounded_copy(buffer, 4, "hello");
    CLINGS_CHECK_INT(copied, 3);
    CLINGS_CHECK_STR(buffer, "hel");
    CLINGS_CHECK_INT(buffer[4], 'X');
    return clings_report();
}
