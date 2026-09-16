/*
 * clings exercise: 12_standard_library/15_rand_max
 * title: RAND_MAX portability
 * objective: Do not assume rand() returns a value below a fixed small bound.
 * hint: The C standard only guarantees RAND_MAX >= 32767.
 */

#include "clings/test.h"

#include <stdlib.h>

int rand_max_is_at_least_32767(void)
{
    return RAND_MAX >= 32767;
}

int bounded_rand(int upper)
{
    return upper > 0 ? rand() % upper : 0;
}

int main(void)
{
    CLINGS_CHECK_INT(rand_max_is_at_least_32767(), 1);
    srand(42u);
    int value = bounded_rand(10);
    CLINGS_CHECK(value >= 0 && value < 10);
    return clings_report();
}
