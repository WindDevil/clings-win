/*
 * clings exercise: 03_types_variables/12_integer_promotions
 * title: Integer promotions
 * objective: See that char operands are promoted to int in arithmetic expressions.
 * hint: sizeof(left + right) is sizeof(int) for char operands.
 */

#include "clings/test.h"

#include <stddef.h>

int char_addition_is_int(void)
{
    char left = 1;
    char right = 2;
    return sizeof(left + right) == sizeof(int);
}

int unsigned_char_promotion(void)
{
    unsigned char value = 255;
    return (int)value + 1;
}

int main(void)
{
    CLINGS_CHECK_INT(char_addition_is_int(), 1);
    CLINGS_CHECK_INT(unsigned_char_promotion(), 256);
    return clings_report();
}
