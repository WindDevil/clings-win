/*
 * clings 练习: 10_aggregates/11_complex_declarations
 * title: 复杂声明与函数指针表
 * objective: 读懂并使用函数指针及其数组的 typedef。
 * hint: binary_operation 是 int (*)(int, int) 的 typedef。
 */

#include "clings/test.h"

typedef int (*binary_operation)(int, int);

static int add(int left, int right)
{
    return left + right;
}

static int subtract(int left, int right)
{
    return left - right;
}

int apply_operation(binary_operation operation, int left, int right)
{
    /* TODO: 调用选中的操作。 */
    return add(left, right);
}

int use_operation_table(void)
{
    binary_operation table[2] = {add, subtract};
    return apply_operation(table[1], 10, 3);
}

int main(void)
{
    CLINGS_CHECK_INT(apply_operation(add, 2, 3), 5);
    CLINGS_CHECK_INT(use_operation_table(), 7);
    return clings_report();
}
