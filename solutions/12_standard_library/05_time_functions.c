/*
 * clings exercise: 12_standard_library/05_time_functions
 * title: Time arithmetic
 * objective: Use time_t and difftime.
 * hint: difftime(end, start) returns end - start seconds.
 */

#include "clings/test.h"

#include <time.h>

long seconds_between(time_t start, time_t end)
{
    return (long)difftime(end, start);
}

int main(void)
{
    CLINGS_CHECK_INT(seconds_between(100, 250), 150);
    CLINGS_CHECK_INT(seconds_between(250, 100), -150);
    return clings_report();
}
