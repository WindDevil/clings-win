/*
 * clings exercise: 15_ub_safety/11_implementation_defined
 * title: Implementation-defined behavior
 * objective: Observe implementation-defined char signedness and packing pragmas.
 * hint: CHAR_MIN tells you whether plain char is signed; #pragma pack changes padding.
 */

#include "clings/test.h"

#include <limits.h>
#include <stddef.h>

int char_is_signed(void)
{
    return CHAR_MIN < 0;
}

int int_width_at_least_16(void)
{
    return (int)(sizeof(int) * CHAR_BIT) >= 16;
}

int packed_size(void)
{
#pragma pack(push, 1)
    struct packed {
        char first;
        int second;
    };
#pragma pack(pop)
    return (int)sizeof(struct packed);
}

int main(void)
{
    CLINGS_CHECK_INT(char_is_signed() == 0 || char_is_signed() == 1, 1);
    CLINGS_CHECK_INT(int_width_at_least_16(), 1);
    CLINGS_CHECK_INT(packed_size(), (int)(sizeof(char) + sizeof(int)));
    return clings_report();
}
