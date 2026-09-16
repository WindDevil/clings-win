/*
 * clings exercise: 08_arrays_strings/17_state_machine
 * title: A small state machine
 * objective: Track state while scanning a string.
 * hint: A word starts when the previous character was whitespace.
 */

#include "clings/test.h"

int count_words(const char *text)
{
    int in_word = 0;
    int words = 0;

    for (const char *p = text; *p != '\0'; ++p) {
        if (*p == ' ' || *p == '\t' || *p == '\n') {
            in_word = 0;
        } else if (!in_word) {
            in_word = 1;
            ++words;
        }
    }
    return words;
}

int main(void)
{
    CLINGS_CHECK_INT(count_words(""), 0);
    CLINGS_CHECK_INT(count_words("hello world"), 2);
    CLINGS_CHECK_INT(count_words("  a\tb\n c  "), 3);
    return clings_report();
}
