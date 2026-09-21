/*
 * clings 练习: 14_file_io/04_getc_putc_ungetc
 * title: getc、putc 与 ungetc
 * objective: 先看一眼字符，再把它放回流里。
 * hint: ungetc 把一个字符退回输入流。
 */

#include "clings/test.h"

#include <stdio.h>

int peek_character(FILE *file)
{
    int character = getc(file);
    if (character != EOF) {
        /* TODO: 把这个字符退回流里。 */
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
