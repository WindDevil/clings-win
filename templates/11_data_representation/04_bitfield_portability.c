/*
 * clings 练习: 11_data_representation/04_bitfield_portability
 * title: 位域与显式掩码
 * objective: 用位域打包字段，并与显式掩码做对比。
 * hint: 位域的布局由实现定义；用掩码能把编码写明确。
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
    /* TODO: 把 4 位的 value 字段掩出来。 */
    flags.value = 0;
    return (int)flags.first | ((int)flags.second << 1) | ((int)flags.value << 2);
}

int main(void)
{
    CLINGS_CHECK_INT(pack_flags(1, 0, 5), 21);
    CLINGS_CHECK_INT(pack_flags(0, 1, 15), 62);
    return clings_report();
}
