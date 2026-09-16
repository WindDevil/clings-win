/*
 * clings exercise: 08_arrays_strings/06_tokenize
 * title: Tokenizing with strtok_r
 * objective: Split a string without modifying the caller's buffer.
 * hint: Pass both space and comma as delimiters.
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
