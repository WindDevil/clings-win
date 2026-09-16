/*
 * clings exercise: 12_standard_library/06_random
 * title: Pseudo-random numbers
 * objective: Seed the generator and bound its output.
 * hint: rand() % upper produces values from 0 to upper - 1.
 */

#include "clings/test.h"

#include <stdlib.h>

void seed_random(unsigned int seed)
{
    srand(seed);
}

int random_bounded(int upper)
{
    return upper > 0 ? rand() % upper : 0;
}

int main(void)
{
    seed_random(42u);
    int first = random_bounded(10);
    seed_random(42u);
    int second = random_bounded(10);

    CLINGS_CHECK_INT(first, second);
    CLINGS_CHECK(first >= 0 && first < 10);
    CLINGS_CHECK_INT(random_bounded(0), 0);
    return clings_report();
}
