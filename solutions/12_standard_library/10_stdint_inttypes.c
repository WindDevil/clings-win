/*
 * clings 练习: 12_standard_library/10_stdint_inttypes
 * title: 定宽整数与格式宏
 * objective: 使用 stdint.h 和 inttypes.h 里的 uint64_t 与 PRIu64。
 * hint: PRIu64 是 uint64_t 的可移植 printf 说明符。
 */

#include "clings/test.h"

#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

int format_u64(char *buffer, size_t size, uint64_t value)
{
    return snprintf(buffer, size, "%" PRIu64, value);
}

uint32_t low_32_bits(uint64_t value)
{
    return (uint32_t)value;
}

int main(void)
{
    char buffer[32];

    CLINGS_CHECK_INT(
        format_u64(buffer, sizeof buffer, UINT64_C(1234567890123)), 13);
    CLINGS_CHECK_STR(buffer, "1234567890123");
    CLINGS_CHECK_INT(low_32_bits(UINT64_C(0x1122334455667788)), 0x55667788u);
    return clings_report();
}
