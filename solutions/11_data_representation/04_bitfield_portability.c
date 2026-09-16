/*
 * clings exercise: 11_data_representation/04_bitfield_portability
 * title: Bitfields and explicit masks
 * objective: Pack fields with bitfields and compare them with an explicit mask.
 * hint: Bitfield layout is implementation-defined; masks make the encoding explicit.
 */

#include "clings/test.h"

struct flags {
    unsigned int first : 1;
    unsigned int second : 1;
    unsigned int value : 4;
};

int pack_flags(int first, int second, int value)
{
    struct flags flags = {0};
    flags.first = first ? 1u : 0u;
    flags.second = second ? 1u : 0u;
    flags.value = (unsigned int)(value & 0x0f);
    return (int)flags.first | ((int)flags.second << 1) | ((int)flags.value << 2);
}

int main(void)
{
    CLINGS_CHECK_INT(pack_flags(1, 0, 5), 21);
    CLINGS_CHECK_INT(pack_flags(0, 1, 15), 62);
    return clings_report();
}
