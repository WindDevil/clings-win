/*
 * clings 练习: 11_data_representation/02_integer_binary_representation
 * title: 整数的位模式
 * objective: 统计置位个数，并把原码转换成补码。
 * hint: value &= value - 1 会清掉最低的那个置位。
 */

#include "clings/test.h"

int count_set_bits(unsigned int value)
{
    int count = 0;
    while (value != 0) {
        /* TODO: 清掉最低的置位。 */
        value >>= 1;
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
