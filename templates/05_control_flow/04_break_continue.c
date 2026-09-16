/*
 * clings 练习: 05_control_flow/04_break_continue
 * title: break 与 continue
 * objective: 用 break 提前结束，用 continue 跳过一轮。
 * hint: continue 跳过本轮剩下的语句；break 直接退出循环。
 */

#include "clings/test.h"

int first_multiple_of_three(int limit)
{
    for (int value = 1; value <= limit; ++value) {
        if (value % 3 == 0) {
            return value;
        }
    }
    return -1;
}

int sum_skipping_multiples_of_three(int limit)
{
    int sum = 0;
    for (int value = 1; value <= limit; ++value) {
        if (value % 3 == 0) {
            /* TODO: 跳过这个值，不要退出循环。 */
            break;
        }
        sum += value;
    }
    return sum;
}

int main(void)
{
    CLINGS_CHECK_INT(first_multiple_of_three(10), 3);
    CLINGS_CHECK_INT(sum_skipping_multiples_of_three(5), 12);
    CLINGS_CHECK_INT(sum_skipping_multiples_of_three(0), 0);
    return clings_report();
}
