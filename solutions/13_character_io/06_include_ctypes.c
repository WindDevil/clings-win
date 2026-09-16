/*
 * clings exercise: 13_character_io/06_include_ctypes
 * title: Include ctype.h
 * objective: Call toupper after including the header that declares it.
 * hint: The compiler needs the declaration from ctype.h; add the include.
 */

#include "clings/test.h"

#include <ctype.h>

int uppercase_a(void)
{
    return toupper('a');
}

int main(void)
{
    CLINGS_CHECK_INT(uppercase_a(), 'A');
    return clings_report();
}
