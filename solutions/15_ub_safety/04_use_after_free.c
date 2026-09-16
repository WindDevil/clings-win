/*
 * clings 练习: 15_ub_safety/04_use_after_free
 * title: 释放后使用
 * objective: 释放目标之后把指针清空。
 * hint: free 之后通过二级指针写入 NULL。
 */

#include "clings/test.h"

#include <stdlib.h>

void free_and_clear(int **pointer)
{
    free(*pointer);
    *pointer = NULL;
}

int is_null(const void *pointer)
{
    return pointer == NULL;
}

int main(void)
{
    int *value = malloc(sizeof *value);

    CLINGS_CHECK(value != NULL);
    *value = 7;
    free_and_clear(&value);
    CLINGS_CHECK_INT(is_null(value), 1);
    return clings_report();
}
