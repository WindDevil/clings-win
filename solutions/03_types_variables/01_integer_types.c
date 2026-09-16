/*
 * clings exercise: 03_types_variables/01_integer_types
 * title: Integer types and ranges
 * objective: Use sizeof, CHAR_BIT, INT_MIN, and INT_MAX correctly.
 * hint: The number of bits in an int is sizeof(int) * CHAR_BIT.
 */

#include "clings/test.h"

#include <limits.h>

int int_bits(void)
{
    return (int)(sizeof(int) * CHAR_BIT);
}

int long_can_hold_int(long value)
{
    return value >= INT_MIN && value <= INT_MAX;
}

int main(void)
{
    CLINGS_CHECK(int_bits() >= 16);
    CLINGS_CHECK_INT(long_can_hold_int(0), 1);
    CLINGS_CHECK_INT(long_can_hold_int((long)INT_MAX), 1);
    {
        /* Data models differ between platforms: LP64 (Linux) keeps
         * INT_MAX in a long, LLP64 (Windows) does not.  Compiling
         * "INT_MAX + 1" as a long is therefore only valid when long
         * is genuinely wider than int. */
        long above_int_max = (long)INT_MAX;
        if (sizeof(long) > sizeof(int)) {
            CLINGS_CHECK_INT(long_can_hold_int(above_int_max + 1), 0);
        } else {
            CLINGS_CHECK_MSG(sizeof(long) == sizeof(int),
                             "long is not wider than int here");
        }
    }
    return clings_report();
}
