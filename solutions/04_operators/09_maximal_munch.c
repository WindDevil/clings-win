/*
 * clings exercise: 04_operators/09_maximal_munch
 * title: Lexical maximal munch
 * objective: Understand how the lexer greedily forms the longest token.
 * hint: a+++b is tokenized as (a++) + b.
 */

#include "clings/test.h"

int greedy_expression(int left, int right)
{
    return left+++right;
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
