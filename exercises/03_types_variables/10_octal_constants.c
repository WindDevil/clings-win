/*
 * clings 练习: 03_types_variables/10_octal_constants
 * title: 八进制整型常量
 * objective: 认识到前导 0 表示八进制。
 * hint: 010 是 8，不是 10；0195 不是合法的 C 整数常量。
 */

#include "clings/test.h"

#include <stdlib.h>

int octal_constant(void)
{
    /* TODO: 返回八进制常量 010。 */
    return 10;
}

int parse_c_integer(const char *text, int *out)
{
    char *end = NULL;
    long value = strtol(text, &end, 0);
    if (end == text || *end != '\0') {
        return -1;
    }
    *out = (int)value;
    return 0;
}

int main(void)
{
    int value = 0;

    CLINGS_CHECK_INT(octal_constant(), 8);
    CLINGS_CHECK_INT(parse_c_integer("010", &value), 0);
    CLINGS_CHECK_INT(value, 8);
    CLINGS_CHECK_INT(parse_c_integer("10", &value), 0);
    CLINGS_CHECK_INT(value, 10);
    CLINGS_CHECK_INT(parse_c_integer("0195", &value), -1);
    return clings_report();
}
