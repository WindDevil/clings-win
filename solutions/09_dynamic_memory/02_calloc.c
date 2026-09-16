/*
 * clings 练习: 09_dynamic_memory/02_calloc
 * title: 零初始化的分配
 * objective: 需要每个字节初值都是零时用 calloc。
 * hint: calloc(count, size) 返回已经清零的内存。
 */

#include "clings/test.h"

#include <stdlib.h>

int *make_zeroed(size_t count)
{
    return calloc(count, sizeof(int));
}

int main(void)
{
    int *values = make_zeroed(5);

    CLINGS_CHECK(values != NULL);
    for (int i = 0; i < 5; ++i) {
        CLINGS_CHECK_INT(values[i], 0);
    }
    free(values);
    return clings_report();
}
