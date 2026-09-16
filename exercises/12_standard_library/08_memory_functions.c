/*
 * clings 练习: 12_standard_library/08_memory_functions
 * title: memcpy、memmove、memset 与 memcmp
 * objective: 正确使用按字节操作的内存函数。
 * hint: memcpy 要求两块内存不重叠；memmove 能处理重叠。
 */

#include "clings/test.h"

#include <string.h>

void copy_ints(int *destination, const int *source, size_t count)
{
    /* TODO: 复制整个数组，不是 count 个字节。 */
    memcpy(destination, source, count);
}

void move_overlapping(char *buffer, size_t size)
{
    memmove(buffer + 1, buffer, size - 1);
}

void clear_ints(int *values, size_t count)
{
    memset(values, 0, count * sizeof *values);
}

int ints_equal(const int *left, const int *right, size_t count)
{
    return memcmp(left, right, count * sizeof *left) == 0;
}

int main(void)
{
    const int source[3] = {1, 2, 3};
    int destination[3] = {0, 0, 0};
    char buffer[6] = "abcde";

    copy_ints(destination, source, 3);
    CLINGS_CHECK_INT(ints_equal(destination, source, 3), 1);
    clear_ints(destination, 3);
    CLINGS_CHECK_INT(destination[0], 0);
    CLINGS_CHECK_INT(destination[2], 0);
    move_overlapping(buffer, 5);
    CLINGS_CHECK_STR(buffer, "aabcd");
    return clings_report();
}
