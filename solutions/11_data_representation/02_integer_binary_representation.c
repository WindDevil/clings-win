/*
 * clings exercise: 11_data_representation/02_integer_binary_representation
 * title: Integer bit patterns
 * objective: Count set bits and convert sign-magnitude to two's complement.
 * hint: value &= value - 1 clears the lowest set bit.
 */

#include "clings/test.h"

int count_set_bits(unsigned int value)
{
    int count = 0;
    while (value != 0) {
        value &= value - 1;
        ++count;
    }
    return count;
}

unsigned int sign_magnitude_to_twos_complement(unsigned int sign_magnitude)
{
    unsigned int sign = sign_magnitude & 0x80000000u;
    unsigned int magnitude = sign_magnitude & 0x7fffffffu;
    return sign ? (~magnitude + 1u) : magnitude;
}

int main(void)
{
    CLINGS_CHECK_INT(count_set_bits(0u), 0);
    CLINGS_CHECK_INT(count_set_bits(0xF0F0u), 8);
    CLINGS_CHECK_INT(sign_magnitude_to_twos_complement(0x80000001u), 0xFFFFFFFFu);
    return clings_report();
}
