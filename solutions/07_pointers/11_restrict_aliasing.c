/*
 * clings exercise: 07_pointers/11_restrict_aliasing
 * title: restrict and aliasing contracts
 * objective: Use restrict to promise that two pointer parameters do not alias.
 * hint: restrict tells the compiler that destination and source do not overlap.
 */

#include "clings/test.h"

#include <stddef.h>

void add_restrict(int *restrict destination, const int *restrict source,
                  size_t count)
{
    for (size_t i = 0; i < count; ++i) {
        destination[i] += source[i];
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
