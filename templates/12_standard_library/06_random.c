/*
 * clings 练习: 12_standard_library/06_random
 * title: 伪随机数
 * objective: 给随机数发生器设种子，并限制输出范围。
 * hint: rand() % upper 得到 0 到 upper - 1 之间的值。
 */

#include "clings/test.h"

#include <stdlib.h>

void seed_random(unsigned int seed)
{
    srand(seed);
}

int random_bounded(int upper)
{
    /* TODO: 让结果落在 upper 以下。 */
    return upper > 0 ? upper : 0;
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
