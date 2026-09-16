/*
 * clings exercise: 17_translation_units/01_header_source_split
 * title: Header and source split
 * objective: Compile a program from a main file, a header, and an implementation file.
 * hint: Declare add in the header and define it in math_utils.c.
 */

#include "clings/test.h"
#include "math_utils.h"

int main(void)
{
    CLINGS_CHECK_INT(add(2, 3), 5);
    CLINGS_CHECK_INT(add(-4, 4), 0);
    return clings_report();
}
