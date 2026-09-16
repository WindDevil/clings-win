/*
 * clings 练习: 11_data_representation/01_base_conversion
 * title: 二进制、八进制与十六进制输入
 * objective: 用 strtoul 解析十六进制字符串。
 * hint: 十六进制可以带 0x 前缀，也可以不带。
 */

#include "clings/test.h"

#include <stdlib.h>

int parse_hex(const char *text, unsigned int *out)
{
    char *end = NULL;
    /* TODO: 按十六进制解析。 */
    unsigned int value = (unsigned int)strtoul(text, &end, 10);
    if (end == text || *end != '\0') {
        return -1;
    }
    *out = value;
    return 0;
}

int main(void)
{
    unsigned int value = 0;

    CLINGS_CHECK_INT(parse_hex("0x2A", &value), 0);
    CLINGS_CHECK_INT(value, 42);
    CLINGS_CHECK_INT(parse_hex("2A", &value), 0);
    CLINGS_CHECK_INT(value, 42);
    CLINGS_CHECK_INT(parse_hex("xyz", &value), -1);
    return clings_report();
}
