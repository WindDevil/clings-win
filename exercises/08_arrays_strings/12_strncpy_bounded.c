/*
 * clings 练习: 08_arrays_strings/12_strncpy_bounded
 * title: 用 strncpy 做有界拷贝
 * objective: 安全复制字符串，并保证目标以 NUL 结尾。
 * hint: 源串过长时，strncpy 不保证结尾有 NUL。
 */

#include "clings/test.h"

#include <stddef.h>
#include <string.h>

int copy_bounded(char *destination, size_t size, const char *source)
{
    if (size == 0) {
        return -1;
    }
    strncpy(destination, source, size - 1);
    /* TODO: 给复制出来的字符串补上结尾。 */
    destination[size - 1] = 'x';
    return 0;
}

int main(void)
{
    char buffer[8];
    char small[4];

    CLINGS_CHECK_INT(copy_bounded(buffer, sizeof buffer, "hello"), 0);
    CLINGS_CHECK_STR(buffer, "hello");
    CLINGS_CHECK_INT(copy_bounded(small, sizeof small, "hello"), 0);
    CLINGS_CHECK_STR(small, "hel");
    CLINGS_CHECK_INT(copy_bounded(buffer, 0, "x"), -1);
    return clings_report();
}
