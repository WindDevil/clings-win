/*
 * clings 练习: 13_character_io/02_eof_ferror
 * title: EOF、feof 与 ferror
 * objective: 读到 EOF，并区分文件结束与读取出错。
 * hint: 只有读取试图越过文件末尾之后，feof 才为真。
 */

#include "clings/test.h"

#include <stdio.h>

int read_all(FILE *file, char *buffer, size_t size)
{
    size_t index = 0;
    int character;
    while (index + 1 < size && (character = fgetc(file)) != EOF) {
        buffer[index] = (char)character;
        ++index;
    }
    buffer[index] = '\0';
    if (ferror(file)) {
        return -1;
    }
    return (int)index;
}

int main(void)
{
    FILE *file = tmpfile();
    char buffer[16];

    CLINGS_CHECK(file != NULL);
    fputs("abc", file);
    rewind(file);
    CLINGS_CHECK_INT(read_all(file, buffer, sizeof buffer), 3);
    CLINGS_CHECK_STR(buffer, "abc");
    /* feof() 只承诺返回非零值。
     * Microsoft CRT 返回的是它内部的标志位（0x10），不是 1。 */
    CLINGS_CHECK_MSG(feof(file) != 0, "feof() reports end-of-file");
    fclose(file);
    return clings_report();
}
