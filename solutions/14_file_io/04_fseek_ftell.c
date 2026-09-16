/*
 * clings 练习: 14_file_io/04_fseek_ftell
 * title: 用 fseek 和 ftell 随机访问
 * objective: 定位到某个字节偏移，并报告结果位置。
 * hint: fseek 配 SEEK_SET 会把流定位到绝对偏移。
 */

#include "clings/test.h"

#include <stdio.h>

int read_at(FILE *file, long offset, char *buffer, size_t size)
{
    if (fseek(file, offset, SEEK_SET) != 0) {
        return -1;
    }
    if (fgets(buffer, (int)size, file) == NULL) {
        return -1;
    }
    return (int)ftell(file);
}

int main(void)
{
    FILE *file = tmpfile();
    char buffer[8];

    CLINGS_CHECK(file != NULL);
    fputs("abcdef", file);
    rewind(file);
    CLINGS_CHECK_INT(read_at(file, 2, buffer, sizeof buffer), 6);
    CLINGS_CHECK_STR(buffer, "cdef");
    fclose(file);
    return clings_report();
}
