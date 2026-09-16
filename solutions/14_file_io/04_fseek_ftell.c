/*
 * clings exercise: 14_file_io/04_fseek_ftell
 * title: Random access with fseek and ftell
 * objective: Seek to a byte offset and report the resulting position.
 * hint: fseek with SEEK_SET positions the stream at an absolute offset.
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
