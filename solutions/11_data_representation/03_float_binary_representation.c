/*
 * clings 练习: 11_data_representation/03_float_binary_representation
 * title: 浮点数的位模式
 * objective: 用 memcpy 查看并还原 IEEE-754 浮点数。
 * hint: 用 memcpy 代替指针强制转换，避开严格别名违规。
 */

#include "clings/test.h"

#include <stdint.h>
#include <string.h>

uint32_t float_bits(float value)
{
    uint32_t bits = 0;
    memcpy(&bits, &value, sizeof bits);
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
