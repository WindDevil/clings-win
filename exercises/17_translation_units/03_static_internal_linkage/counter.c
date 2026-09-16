#include "counter.h"

static int count = 0;

int next_count(void)
{
    /* TODO: 前置自增这个私有计数器。 */
    return count++;
}

int count_calls(void)
{
    return count;
}
