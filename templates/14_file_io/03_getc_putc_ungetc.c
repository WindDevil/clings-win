/*
 * clings exercise: 14_file_io/03_getc_putc_ungetc
 * title: getc, putc, and ungetc
 * objective: Peek at a character and put it back into the stream.
 * hint: ungetc pushes one character back onto the input stream.
 */

#include "clings/test.h"

#include <stdio.h>

int peek_character(FILE *file)
{
    int character = getc(file);
    if (character != EOF) {
        /* TODO: put the character back into the stream. */
    }
    return character;
}

int main(void)
{
    FILE *file = tmpfile();

    CLINGS_CHECK(file != NULL);
    fputs("abc", file);
    rewind(file);
    CLINGS_CHECK_INT(peek_character(file), 'a');
    CLINGS_CHECK_INT(peek_character(file), 'a');
    CLINGS_CHECK_INT(getc(file), 'a');
    fclose(file);
    return clings_report();
}
