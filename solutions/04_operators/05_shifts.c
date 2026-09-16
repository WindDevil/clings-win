/*
 * clings exercise: 04_operators/05_shifts
 * title: Shift operators and masks
 * objective: Build masks and avoid shifting by the width of the type.
 * hint: A mask of width w has w low bits set: (1u << w) - 1u.
 */

#include "clings/test.h"

unsigned low_bits_mask(unsigned width)
{
    return (width == 0u) ? 0u : ((1u << width) - 1u);
}

unsigned shift_left_safe(unsigned value, unsigned count)
{
    return (count >= 32u) ? 0u : value << count;
}

int main(void)
{
    CLINGS_CHECK_INT(low_bits_mask(0u), 0u);
    CLINGS_CHECK_INT(low_bits_mask(4u), 0xFu);
    CLINGS_CHECK_INT(shift_left_safe(1u, 4u), 16u);
    CLINGS_CHECK_INT(shift_left_safe(1u, 32u), 0u);
    return clings_report();
}
