/*
 * clings exercise: 03_types_variables/11_char_signedness
 * title: char signedness
 * objective: Use signed char and unsigned char explicitly when the sign matters.
 * hint: Plain char may be signed or unsigned; signed char and unsigned char are explicit.
 */

#include "clings/test.h"

int signed_char_value(signed char value)
{
    return value;
}

int unsigned_char_value(unsigned char value)
{
    return value;
}

int main(void)
{
    CLINGS_CHECK_INT(signed_char_value((signed char)0xFF), -1);
    CLINGS_CHECK_INT(unsigned_char_value((unsigned char)0xFF), 255);
    return clings_report();
}
