/*
 * clings exercise: 13_character_io/01_getc_putc
 * title: getc and putc
 * objective: Copy a stream one character at a time with getc and putc.
 * hint: getc returns EOF when there are no more characters.
 */

#include "clings/test.h"

#include <stdio.h>

int copy_stream(FILE *input, FILE *output)
{
    int character;
    int count = 0;
    while ((character = getc(input)) != EOF) {
        /* TODO: write the current character. */
        putc('x', output);
        ++count;
    }
    return count;
}

int main(void)
{
    FILE *input = tmpfile();
    FILE *output = tmpfile();
    char buffer[16];

    CLINGS_CHECK(input != NULL && output != NULL);
    fputs("hello", input);
    rewind(input);
    CLINGS_CHECK_INT(copy_stream(input, output), 5);
    rewind(output);
    CLINGS_CHECK(fgets(buffer, sizeof buffer, output) != NULL);
    CLINGS_CHECK_STR(buffer, "hello");
    fclose(input);
    fclose(output);
    return clings_report();
}
