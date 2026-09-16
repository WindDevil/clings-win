/*
 * clings 练习: 09_dynamic_memory/01_malloc_free
 * title: 分配、初始化与释放
 * objective: 用 malloc 和 free 管理动态长度的数组。
 * hint: 每个元素都要写入 fill，不能只写第一个。
 */

#include "clings/test.h"

#include <stdlib.h>

int *make_array(size_t count, int fill)
{
    int *values = malloc(count * sizeof *values);
    if (values == NULL) {
        return NULL;
    }
    for (size_t i = 0; i < count; ++i) {
        /* TODO: 初始化当前元素。 */
        values[i] = 0;
    }
    return values;
}

void destroy_array(int *values)
{
    free(values);
}

int main(void)
{
    int *values = make_array(4, 7);

    CLINGS_CHECK(values != NULL);
    CLINGS_CHECK_INT(values[0], 7);
    CLINGS_CHECK_INT(values[1], 7);
    CLINGS_CHECK_INT(values[3], 7);
    destroy_array(values);
    return clings_report();
}
