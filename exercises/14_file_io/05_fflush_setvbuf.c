/*
 * clings exercise: 14_file_io/05_fflush_setvbuf
 * title: Stream buffering
 * objective: Configure full buffering and flush a stream.
 * hint: setvbuf must be called before other I/O on the stream.
 */

#include "clings/test.h"

#include <stdio.h>

int configure_buffer(FILE *file, char *buffer, size_t size)
{
    return setvbuf(file, buffer, _IOFBF, size) == 0 ? 0 : -1;
}

int flush_output(FILE *file)
{
    /* TODO: flush the stream. */
    return -1;
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
