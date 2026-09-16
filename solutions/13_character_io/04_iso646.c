/*
 * clings exercise: 13_character_io/04_iso646
 * title: iso646.h alternative spellings
 * objective: Use and/or/not from iso646.h.
 * hint: iso646.h defines and as && and or as ||.
 */

#include "clings/test.h"

#include <iso646.h>

int is_yes(const char *text)
{
    return (text[0] == 'y' or text[0] == 'Y') and text[1] == '\0';
}

int main(void)
{
    CLINGS_CHECK_INT(is_yes("y"), 1);
    CLINGS_CHECK_INT(is_yes("Y"), 1);
    CLINGS_CHECK_INT(is_yes("yes"), 0);
    CLINGS_CHECK_INT(is_yes("n"), 0);
    return clings_report();
}
