/*
 * clings exercise: 15_ub_safety/06_strict_aliasing
 * title: Type punning without strict-aliasing violations
 * objective: Reinterpret object representation with memcpy.
 * hint: memcpy preserves the bit pattern; a cast to float converts the numeric value.
 */

#include "clings/test.h"

#include <string.h>

float bits_to_float(unsigned int bits)
{
    float value;
    memcpy(&value, &bits, sizeof value);
    return value;
}

int main(void)
{
    CLINGS_CHECK_INT(bits_to_float(0x3f800000u) == 1.0f, 1);
    CLINGS_CHECK_INT(bits_to_float(0x00000000u) == 0.0f, 1);
    return clings_report();
}
