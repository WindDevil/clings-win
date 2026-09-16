/*
 * clings exercise: 12_standard_library/10_stdint_inttypes
 * title: Fixed-width integers and format macros
 * objective: Use uint64_t and PRIu64 from stdint.h and inttypes.h.
 * hint: PRIu64 is the portable printf specifier for uint64_t.
 */

#include "clings/test.h"

#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

int format_u64(char *buffer, size_t size, uint64_t value)
{
    /* TODO: use the format macro for uint64_t. */
    return snprintf(buffer, size, "%" PRIu32, value);
}

uint32_t low_32_bits(uint64_t value)
{
    return (uint32_t)value;
}

int main(void)
{
    char buffer[32];

    CLINGS_CHECK_INT(
        format_u64(buffer, sizeof buffer, UINT64_C(1234567890123)), 13);
    CLINGS_CHECK_STR(buffer, "1234567890123");
    CLINGS_CHECK_INT(low_32_bits(UINT64_C(0x1122334455667788)), 0x55667788u);
    return clings_report();
}
