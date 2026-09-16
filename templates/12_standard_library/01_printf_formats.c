/*
 * clings 练习: 12_standard_library/01_printf_formats
 * title: printf 格式说明符
 * objective: 让每个转换说明符与实参类型匹配。
 * hint: long 用 %ld；double 用 %f 或 %.2f。
 */

#include "clings/test.h"

#include <stdio.h>

int format_all(char *buffer, size_t size, long value, double real,
               const char *text)
{
    /* TODO: 用 long 对应的说明符。 */
    return snprintf(buffer, size, "%d %.2f %s", value, real, text);
}

int main(void)
{
    char buffer[64];

    CLINGS_CHECK_INT(format_all(buffer, sizeof buffer, 42L, 3.5, "ok"), 10);
    CLINGS_CHECK_STR(buffer, "42 3.50 ok");
    return clings_report();
}
