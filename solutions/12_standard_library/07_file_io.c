/*
 * clings exercise: 12_standard_library/07_file_io
 * title: Text file I/O
 * objective: Write and read a text file with fopen, fputs, and fread.
 * hint: Use mode "w" for writing and mode "r" for reading.
 */

#include "clings/test.h"

#include <stdio.h>

int write_text_file(const char *path, const char *text)
{
    FILE *file = fopen(path, "w");
    if (file == NULL) {
        return -1;
    }
    int ok = fputs(text, file) >= 0;
    if (fclose(file) != 0) {
        ok = 0;
    }
    return ok ? 0 : -1;
}

int read_text_file(const char *path, char *buffer, size_t size)
{
    FILE *file = fopen(path, "r");
    if (file == NULL) {
        return -1;
    }
    size_t count = fread(buffer, 1, size - 1, file);
    buffer[count] = '\0';
    fclose(file);
    return (int)count;
}

int main(void)
{
    const char *path = "/tmp/clings_file_io_test.txt";
    char buffer[32];

    CLINGS_CHECK_INT(write_text_file(path, "hello"), 0);
    CLINGS_CHECK_INT(read_text_file(path, buffer, sizeof buffer), 5);
    CLINGS_CHECK_STR(buffer, "hello");
    remove(path);
    return clings_report();
}
