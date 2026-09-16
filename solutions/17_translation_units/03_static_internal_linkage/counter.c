#include "counter.h"

static int count = 0;

int next_count(void)
{
    return ++count;
}

int count_calls(void)
{
    return count;
}
