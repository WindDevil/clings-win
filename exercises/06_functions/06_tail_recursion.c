/*
 * clings 练习: 06_functions/06_tail_recursion
 * title: 尾递归
 * objective: 用累加器改写递归求和。
 * hint: 递归调用应当是这个函数里最后一步操作。
 */

#include "clings/test.h"

static int sum_tail(int value, int accumulator)
{
    return value == 0 ? accumulator : /* TODO: add the current value to the accumulator. */
        sum_tail(value - 1, accumulator);
}

int sum_tail_wrapper(int value)
{
    return sum_tail(value, 0);
}

int main(void)
{
    CLINGS_CHECK_INT(sum_tail_wrapper(0), 0);
    CLINGS_CHECK_INT(sum_tail_wrapper(5), 15);
    CLINGS_CHECK_INT(sum_tail_wrapper(10), 55);
    return clings_report();
}
