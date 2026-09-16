/*
 * clings exercise: 11_data_representation/03_float_binary_representation
 * title: Floating-point bit patterns
 * objective: Inspect and reconstruct an IEEE-754 float with memcpy.
 * hint: Use memcpy instead of pointer casts to avoid strict-aliasing violations.
 */

#include "clings/test.h"

#include <stdint.h>
#include <string.h>

uint32_t float_bits(float value)
{
    uint32_t bits = 0;
    /* TODO: copy the object representation. */
    bits = (uint32_t)value;
    return bits;
}

float bits_to_float(uint32_t bits)
{
    float value = 0.0f;
    memcpy(&value, &bits, sizeof value);
    return value;
}

int main(void)
{
    CLINGS_CHECK_INT(float_bits(1.0f), 0x3f800000u);
    CLINGS_CHECK_INT(bits_to_float(0x3f800000u) == 1.0f, 1);
    return clings_report();
}
