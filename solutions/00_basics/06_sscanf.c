/*
 * clings 练习: 00_basics/06_sscanf
 * title: 用 sscanf 安全解析
 * objective: 用 sscanf 从字符串里解析出各个值。
 * hint: 格式串里的那个逗号必须和输入串里的对齐。
 */

#include "clings/test.h"

#include <stdio.h>

int first;
int second;

int parse_pair(void)
{
    return sscanf("3,4", "%d,%d", &first, &second) == 2 ? 0 : -1;
}

int parse_invalid(void)
{
    return sscanf("3 4", "%d,%d", &first, &second) == 2 ? 0 : -1;
}

int main(void)
{
    CLINGS_CHECK_INT(parse_pair(), 0);
    CLINGS_CHECK_INT(first, 3);
    CLINGS_CHECK_INT(second, 4);
    CLINGS_CHECK_INT(parse_invalid(), -1);
    return clings_report();
}
