/*
 * clings exercise: 14_file_io/07_buffered_output_memory
 * title: Buffered output and memory allocation
 * objective: Combine malloc, setvbuf, output, fclose, and free.
 * hint: The buffer passed to setvbuf must remain valid until the stream is closed.
 */

#include "clings/test.h"

#include <stdio.h>
#include <stdlib.h>

int write_with_buffer(const char *path, const char *text, size_t size)
{
    FILE *file = fopen(path, "w");
    if (file == NULL) {
        return -1;
    }
    char *buffer = malloc(size);
    if (buffer == NULL) {
        fclose(file);
        return -1;
    }
    if (setvbuf(file, buffer, _IOFBF, size) != 0) {
        free(buffer);
        fclose(file);
        return -1;
    }
    /* TODO: write the supplied text. */
    int ok = fputs("wrong", file) >= 0;
    if (fclose(file) != 0) {
        ok = 0;
    }
    free(buffer);
    return ok ? 0 : -1;
}

int main(void)
{
    const char *path = "/tmp/clings_buffered_output.txt";
    char buffer[32];

    CLINGS_CHECK_INT(write_with_buffer(path, "buffered", 128), 0);
    FILE *file = fopen(path, "r");
    CLINGS_CHECK(file != NULL);
    CLINGS_CHECK(fgets(buffer, sizeof buffer, file) != NULL);
    CLINGS_CHECK_STR(buffer, "buffered");
    fclose(file);
    remove(path);
    return clings_report();
}
