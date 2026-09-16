/*
 * clings 练习: 07_pointers/06_dangling_wild
 * title: 野指针与安全释放
 * objective: 释放后把指针置为 NULL，防止误用。
 * hint: free(*pointer) 之后，通过二级指针把它置为 NULL。
 */

#include "clings/test.h"

#include <stdlib.h>

void safe_free(int **pointer)
{
    free(*pointer);
    /* TODO: 释放之后把调用方的指针置空。 */
}

int is_null(const void *pointer)
{
    return pointer == NULL;
}

int main(void)
{
    int *value = malloc(sizeof *value);

    CLINGS_CHECK(value != NULL);
    *value = 42;
    safe_free(&value);
    CLINGS_CHECK_INT(is_null(value), 1);
    return clings_report();
}
