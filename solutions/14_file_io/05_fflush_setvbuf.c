/*
 * clings 练习: 14_file_io/05_fflush_setvbuf
 * title: 流缓冲
 * objective: 配置全缓冲并刷新流。
 * hint: 必须在流上做其它 I/O 之前调用 setvbuf。
 */

#include "clings/test.h"

#include <stdio.h>

int configure_buffer(FILE *file, char *buffer, size_t size)
{
    return setvbuf(file, buffer, _IOFBF, size) == 0 ? 0 : -1;
}

int flush_output(FILE *file)
{
    return fflush(file) == 0 ? 0 : -1;
}

int main(void)
{
    FILE *file = tmpfile();
    char buffer[128];

    CLINGS_CHECK(file != NULL);
    CLINGS_CHECK_INT(configure_buffer(file, buffer, sizeof buffer), 0);
    CLINGS_CHECK_INT(fputs("buffered", file) >= 0, 1);
    CLINGS_CHECK_INT(flush_output(file), 0);
    fclose(file);
    return clings_report();
}
