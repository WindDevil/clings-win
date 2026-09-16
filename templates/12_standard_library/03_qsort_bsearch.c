/*
 * clings 练习: 12_standard_library/03_qsort_bsearch
 * title: qsort 与 bsearch
 * objective: 用比较回调配合排序和查找。
 * hint: 比较函数返回负数、零或正数。
 */

#include "clings/test.h"

#include <stdlib.h>

static int compare_ints(const void *left, const void *right)
{
    int a = *(const int *)left;
    int b = *(const int *)right;
    /* TODO: 返回升序。 */
    return (a < b) - (a > b);
}

void sort_ints(int *values, size_t count)
{
    qsort(values, count, sizeof *values, compare_ints);
}

int *find_int(int *values, size_t count, int needle)
{
    return bsearch(&needle, values, count, sizeof *values, compare_ints);
}

int main(void)
{
    int values[] = {4, 1, 3, 2};
    int needle = 3;

    sort_ints(values, 4);
    CLINGS_CHECK_INT(values[0], 1);
    CLINGS_CHECK_INT(values[1], 2);
    CLINGS_CHECK_INT(values[2], 3);
    CLINGS_CHECK_INT(values[3], 4);
    CLINGS_CHECK(find_int(values, 4, needle) != NULL);
    CLINGS_CHECK(find_int(values, 4, 99) == NULL);
    return clings_report();
}
