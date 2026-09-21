/*
 * clings 练习: 12_standard_library/12_scanf_advanced
 * title: scanf 输入进阶
 * objective: 在 sscanf 里使用字段宽度和扫描集。
 * hint: %3d 最多读三位数字；%[abc] 只读 a、b、c。
 */

#include "clings/test.h"

#include <stdio.h>

int parse_field(const char *input, int *out)
{
    /* TODO: 最多读三位数字。 */
    return sscanf(input, "%d", out) == 1 ? 0 : -1;
}

int parse_set(const char *input, char *out, size_t size)
{
    if (size == 0) {
        return -1;
    }
    out[0] = '\0';
    return sscanf(input, "%[abc]", out) == 1 ? 0 : -1;
}

int main(void)
{
    int value = 0;
    char buffer[16];

    CLINGS_CHECK_INT(parse_field("12345", &value), 0);
    CLINGS_CHECK_INT(value, 123);
    CLINGS_CHECK_INT(parse_set("abcxyz", buffer, sizeof buffer), 0);
    CLINGS_CHECK_STR(buffer, "abc");
    CLINGS_CHECK_INT(parse_set("xyz", buffer, sizeof buffer), -1);
    return clings_report();
}
