/*
 * clings exercise: 07_pointers/08_null_empty_string
 * title: NULL, empty string, and NUL
 * objective: Distinguish a null pointer, an empty string, and the NUL character.
 * hint: NULL is a null pointer; "" is a valid empty string; '\0' is NUL.
 */

#include "clings/test.h"

#include <stddef.h>
#include <string.h>

int length_or_zero(const char *text)
{
    return text == NULL ? 0 : (int)strlen(text);
}

int is_empty_string(const char *text)
{
    return text != NULL && text[0] == '\0';
}

int main(void)
{
    CLINGS_CHECK_INT(length_or_zero(NULL), 0);
    CLINGS_CHECK_INT(length_or_zero(""), 0);
    CLINGS_CHECK_INT(is_empty_string(""), 1);
    CLINGS_CHECK_INT(is_empty_string(NULL), 0);
    return clings_report();
}
