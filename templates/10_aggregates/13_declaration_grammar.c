/*
 * clings 练习: 10_aggregates/13_declaration_grammar
 * title: 声明文法与函数指针表
 * objective: 读懂函数指针数组的 typedef。
 * hint: operation_table 是 typedef int (*[3])(int, int)。
 */

#include "clings/test.h"

typedef int (*binary_operation)(int, int);
typedef binary_operation operation_table[3];

static int add(int left, int right)
{
    return left + right;
}

static int subtract(int left, int right)
{
    return left - right;
}

static int multiply(int left, int right)
{
    return left * right;
}

int apply_table(operation_table table, int index, int left, int right)
{
    /* TODO: 调用表中选中的那一项。 */
    return table[0](left, right);
}

int declaration_demo(void)
{
    operation_table table = {add, subtract, multiply};
    return apply_table(table, 1, 10, 3);
}

int main(void)
{
    operation_table table = {add, subtract, multiply};

    CLINGS_CHECK_INT(apply_table(table, 0, 2, 3), 5);
    CLINGS_CHECK_INT(apply_table(table, 1, 10, 3), 7);
    CLINGS_CHECK_INT(apply_table(table, 2, 10, 3), 30);
    CLINGS_CHECK_INT(declaration_demo(), 7);
    return clings_report();
}
