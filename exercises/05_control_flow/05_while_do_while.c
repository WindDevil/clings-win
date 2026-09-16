/*
 * clings exercise: 05_control_flow/05_while_do_while
 * title: while and do-while
 * objective: Distinguish entry-condition and exit-condition loops.
 * hint: A do-while body always executes at least once.
 */

#include "clings/test.h"

int sum_while(int limit)
{
    int sum = 0;
    int value = 1;
    while (value <= limit) {
        sum += value;
        ++value;
    }
    return sum;
}

int count_do_while(int limit)
{
    int count = 0;
    /* TODO: use an exit-condition loop. */
    while (count < limit) {
        ++count;
    }
    return count;
}

int main(void)
{
    CLINGS_CHECK_INT(sum_while(0), 0);
    CLINGS_CHECK_INT(sum_while(5), 15);
    CLINGS_CHECK_INT(count_do_while(0), 1);
    CLINGS_CHECK_INT(count_do_while(3), 3);
    return clings_report();
}
