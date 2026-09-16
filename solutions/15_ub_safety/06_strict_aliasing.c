/*
 * clings 练习: 15_ub_safety/06_strict_aliasing
 * title: 不做违反严格别名规则的类型双关
 * objective: 用 memcpy 重新解释对象的表示。
 * hint: memcpy 保留位模式；强制转换成 float 则是转换数值。
 */

#include "clings/test.h"

#include <string.h>

float bits_to_float(unsigned int bits)
{
    float value;
    memcpy(&value, &bits, sizeof value);
    return value;
}

int main(void)
{
    CLINGS_CHECK_INT(bits_to_float(0x3f800000u) == 1.0f, 1);
    CLINGS_CHECK_INT(bits_to_float(0x00000000u) == 0.0f, 1);
    return clings_report();
}
