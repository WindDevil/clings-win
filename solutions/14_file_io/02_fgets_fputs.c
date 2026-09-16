/*
 * clings exercise: 14_file_io/02_fgets_fputs
 * title: fgets and fputs
 * objective: Copy a text file line by line.
 * hint: fgets includes the newline when the buffer is large enough.
 */

#include "clings/test.h"

#include <stdio.h>

int copy_lines(FILE *input, FILE *output)
{
    char buffer[64];
    int count = 0;
    while (fgets(buffer, sizeof buffer, input) != NULL) {
        if (fputs(buffer, output) == EOF) {
            return -1;
        }
        ++count;
    }
    return count;
}

int main(void)
{
    FILE *input = tmpfile();
    FILE *output = tmpfile();
    char buffer[64];

    CLINGS_CHECK(input != NULL && output != NULL);
    fputs("first\nsecond\n", input);
    rewind(input);
    CLINGS_CHECK_INT(copy_lines(input, output), 2);
    rewind(output);
    CLINGS_CHECK(fgets(buffer, sizeof buffer, output) != NULL);
    CLINGS_CHECK_STR(buffer, "first\n");
    CLINGS_CHECK(fgets(buffer, sizeof buffer, output) != NULL);
    CLINGS_CHECK_STR(buffer, "second\n");
    fclose(input);
    fclose(output);
    return clings_report();
}
