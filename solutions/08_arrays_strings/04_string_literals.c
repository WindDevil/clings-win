/*
 * clings exercise: 08_arrays_strings/04_string_literals
 * title: String literals and mutable strings
 * objective: Scan a const string and modify a mutable char array.
 * hint: A string literal must not be modified; a char array may be modified.
 */

#include "clings/test.h"

int count_vowels(const char *text)
{
    int count = 0;
    for (const char *p = text; *p != '\0'; ++p) {
        switch (*p) {
        case 'a':
        case 'e':
        case 'i':
        case 'o':
        case 'u':
            ++count;
            break;
        default:
            break;
        }
    }
    return count;
}

void replace_char(char *text, char from, char to)
{
    for (char *p = text; *p != '\0'; ++p) {
        if (*p == from) {
            *p = to;
        }
    }
}

int main(void)
{
    char text[] = "hello";

    CLINGS_CHECK_INT(count_vowels("hello"), 2);
    replace_char(text, 'l', 'L');
    CLINGS_CHECK_STR(text, "heLLo");
    return clings_report();
}
