/*
 * clings exercise: 03_types_variables/02_signed_unsigned
 * title: Signed and unsigned conversions
 * objective: Avoid the usual arithmetic conversion trap when comparing.
 * hint: A negative int converted to unsigned becomes a very large value.
 */

#include "clings/test.h"

int compare_int_unsigned(int a, unsigned b)
{
    if (a < 0) {
        return -1;
    }
    if ((unsigned)a < b) {
        return -1;
    }
    if ((unsigned)a > b) {
        return 1;
    }
    return 0;
}

int main(void)
{
    CLINGS_CHECK_INT(compare_int_unsigned(-1, 0u), -1);
    CLINGS_CHECK_INT(compare_int_unsigned(5, 3u), 1);
    CLINGS_CHECK_INT(compare_int_unsigned(3, 3u), 0);
    CLINGS_CHECK_INT(compare_int_unsigned(2, 9u), -1);
    return clings_report();
}
