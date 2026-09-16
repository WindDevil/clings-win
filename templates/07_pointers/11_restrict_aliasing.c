/*
 * clings 练习: 07_pointers/11_restrict_aliasing
 * title: restrict 与别名约定
 * objective: 用 restrict 承诺两个指针参数不互相别名。
 * hint: restrict 告诉编译器，目标和源不会重叠。
 */

#include "clings/test.h"

#include <stddef.h>

void add_restrict(int *restrict destination, const int *restrict source,
                  size_t count)
{
    for (size_t i = 0; i < count; ++i) {
        /* TODO: 用对应的源元素。 */
        destination[i] += source[0];
    }
}

int restrict_demo(void)
{
    int values[4] = {1, 2, 3, 4};
    int source[4] = {10, 20, 30, 40};
    add_restrict(values, source, 4);
    return values[0] + values[3];
}

int main(void)
{
    CLINGS_CHECK_INT(restrict_demo(), 55);
    return clings_report();
}
