/*
 * clings exercise: 00_basics/04_char_array
 * title: Character arrays
 * objective: Store text in a char array and access its characters.
 * hint: Array indexes start at 0; sizeof("hello") includes the terminating NUL.
 */

#include "clings/test.h"

char text[] = "hello";

char first_character(void)
{
    return text[0];
}

char last_character(void)
{
    return text[4];
}

int main(void)
{
    CLINGS_CHECK_INT(first_character(), 'h');
    CLINGS_CHECK_INT(last_character(), 'o');
    return clings_report();
}
