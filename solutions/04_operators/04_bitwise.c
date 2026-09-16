/*
 * clings exercise: 04_operators/04_bitwise
 * title: Bitwise set, clear, toggle, and test
 * objective: Use masks and bitwise operators safely.
 * hint: Clearing a bit uses value & ~(1u << bit).
 */

#include "clings/test.h"

unsigned set_bit(unsigned value, unsigned bit)
{
    return value | (1u << bit);
}

unsigned clear_bit(unsigned value, unsigned bit)
{
    return value & ~(1u << bit);
}

unsigned toggle_bit(unsigned value, unsigned bit)
{
    return value ^ (1u << bit);
}

int test_bit(unsigned value, unsigned bit)
{
    return (value & (1u << bit)) != 0;
}

int main(void)
{
    CLINGS_CHECK_INT(set_bit(0u, 3u), 8u);
    CLINGS_CHECK_INT(clear_bit(0xFu, 2u), 0xBu);
    CLINGS_CHECK_INT(toggle_bit(0xFu, 0u), 0xEu);
    CLINGS_CHECK_INT(test_bit(0x8u, 3u), 1);
    CLINGS_CHECK_INT(test_bit(0x8u, 2u), 0);
    return clings_report();
}
