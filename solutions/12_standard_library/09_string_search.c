/*
 * clings exercise: 12_standard_library/09_string_search
 * title: Searching strings
 * objective: Use strchr, strrchr, and strstr.
 * hint: strstr finds a substring, not just a single character.
 */

#include "clings/test.h"

#include <string.h>

const char *find_first(const char *text, char character)
{
    return strchr(text, character);
}

const char *find_last(const char *text, char character)
{
    return strrchr(text, character);
}

const char *find_substring(const char *text, const char *needle)
{
    return strstr(text, needle);
}

int main(void)
{
    const char *text = "hello world";

    CLINGS_CHECK(find_first(text, 'l') == text + 2);
    CLINGS_CHECK(find_last(text, 'l') == text + 9);
    CLINGS_CHECK(find_substring(text, "or") == text + 7);
    CLINGS_CHECK(find_substring(text, "xyz") == NULL);
    return clings_report();
}
