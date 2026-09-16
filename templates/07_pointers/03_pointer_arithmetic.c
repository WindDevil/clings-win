/*
 * clings 练习: 07_pointers/03_pointer_arithmetic
 * title: 指针运算
 * objective: 用指针遍历数组，并返回指向数组内部的指针。
 * hint: 每次前进一个元素；结束条件是 p < values + count。
 */

#include "clings/test.h"

#include <stddef.h>

int sum_pointer(const int *values, int count)
{
    int sum = 0;
    /* TODO: 访问到每一个元素。 */
    for (const int *p = values; p < values + count; p += 2) {
        sum += *p;
    }
    return sum;
}

const int *find_value(const int *values, int count, int needle)
{
    for (const int *p = values; p < values + count; ++p) {
        if (*p == needle) {
            return p;
        }
    }
    return NULL;
}

int main(void)
{
    const int values[] = {10, 20, 30, 40};
    const int *found = find_value(values, 4, 30);

    CLINGS_CHECK_INT(sum_pointer(values, 4), 100);
    CLINGS_CHECK(found != NULL);
    CLINGS_CHECK_INT((int)(found - values), 2);
    CLINGS_CHECK(find_value(values, 4, 99) == NULL);
    return clings_report();
}
