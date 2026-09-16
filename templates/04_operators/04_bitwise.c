/*
 * clings 练习: 04_operators/04_bitwise
 * title: 位操作：置位、清位、取反与测试
 * objective: 安全地使用掩码和位运算符。
 * hint: 清位用 value & ~(1u << bit)。
 */

#include "clings/test.h"

unsigned set_bit(unsigned value, unsigned bit)
{
    return value | (1u << bit);
}

unsigned clear_bit(unsigned value, unsigned bit)
{
    /* TODO: 清掉选中的那一位置位。 */
    return value & (1u << bit);
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
