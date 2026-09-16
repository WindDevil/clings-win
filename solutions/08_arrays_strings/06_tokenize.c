/*
 * clings 练习: 08_arrays_strings/06_tokenize
 * title: 用 strtok_r 分词
 * objective: 切分字符串，同时不改动调用方的缓冲区。
 * hint: 空格和逗号都要作为分隔符传进去。
 */

#include "clings/test.h"

#include <stdlib.h>
#include <string.h>

int count_tokens(const char *text)
{
    char *copy = malloc(strlen(text) + 1);
    if (copy == NULL) {
        return -1;
    }
    strcpy(copy, text);

    int count = 0;
    char *save = NULL;
    for (char *token = strtok_r(copy, " ,", &save); token != NULL;
         token = strtok_r(NULL, " ,", &save)) {
        ++count;
    }

    free(copy);
    return count;
}

int main(void)
{
    CLINGS_CHECK_INT(count_tokens("one,two three"), 3);
    CLINGS_CHECK_INT(count_tokens("  a , b ,c  "), 3);
    CLINGS_CHECK_INT(count_tokens(""), 0);
    return clings_report();
}
