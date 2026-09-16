/*
 * clings exercise: 08_arrays_strings/05_string_ops
 * title: Implementing string operations
 * objective: Implement strlen, strcmp, and strcpy with pointers.
 * hint: The destination pointer must advance after each copied character.
 */

#include "clings/test.h"

#include <stddef.h>

size_t my_strlen(const char *text)
{
    const char *p = text;
    while (*p != '\0') {
        ++p;
    }
    return (size_t)(p - text);
}

int my_strcmp(const char *left, const char *right)
{
    while (*left != '\0' && *left == *right) {
        ++left;
        ++right;
    }
    return (int)(unsigned char)*left - (int)(unsigned char)*right;
}

char *my_strcpy(char *destination, const char *source)
{
    char *result = destination;
    /* TODO: copy until the terminating NUL. */
    while ((*destination++ = *source++) == '\0') {
    }
    return result;
}

int main(void)
{
    char buffer[16];

    CLINGS_CHECK_INT(my_strlen("hello"), 5);
    CLINGS_CHECK_INT(my_strlen(""), 0);
    CLINGS_CHECK_INT(my_strcmp("abc", "abc"), 0);
    CLINGS_CHECK(my_strcmp("abc", "abd") < 0);
    CLINGS_CHECK_STR(my_strcpy(buffer, "copy me"), "copy me");
    return clings_report();
}
