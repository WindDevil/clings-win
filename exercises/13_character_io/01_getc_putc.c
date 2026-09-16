/*
 * clings 练习: 13_character_io/01_getc_putc
 * title: getc 与 putc
 * objective: 用 getc 和 putc 逐字符复制流。
 * hint: 没有字符可读时，getc 返回 EOF。
 */

#include "clings/test.h"

#include <stdio.h>

int copy_stream(FILE *input, FILE *output)
{
    int character;
    int count = 0;
    while ((character = getc(input)) != EOF) {
        /* TODO: 写出当前字符。 */
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
