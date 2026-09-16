#include "counter.h"

static int count = 0;

int next_count(void)
{
    /* TODO: pre-increment the private counter. */
    return count++;
}

int count_calls(void)
{
    return count;
}
