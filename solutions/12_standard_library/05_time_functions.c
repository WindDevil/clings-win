/*
 * clings 练习: 12_standard_library/05_time_functions
 * title: 时间运算
 * objective: 使用 time_t 和 difftime。
 * hint: difftime(end, start) 返回 end - start 秒。
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
