/*
 * clings 练习: 04_operators/09_maximal_munch
 * title: 词法最长匹配
 * objective: 理解词法分析如何贪心地构成最长的记号。
 * hint: a+++b 会被切分成 (a++) + b。
 */

#include "clings/test.h"

int greedy_expression(int left, int right)
{
    /* TODO: 保持最长匹配的切分结果。 */
    return left + ++right;
}

int comment_expression(void)
{
    return 1 /* comment */ + 2;
}

int main(void)
{
    CLINGS_CHECK_INT(greedy_expression(1, 2), 3);
    CLINGS_CHECK_INT(comment_expression(), 3);
    return clings_report();
}
