/*
 * clings 练习: 07_pointers/13_function_pointers
 * title: 函数指针与分派
 * objective: 把函数存进变量，在运行时选一个调用。
 * hint: 返回与运算符字符对应的那个函数。
 */

#include "clings/test.h"

typedef int (*operation_fn)(int, int);

static int add(int a, int b)
{
    return a + b;
}

static int multiply(int a, int b)
{
    return a * b;
}

int apply_operation(operation_fn op, int a, int b)
{
    return op(a, b);
}

operation_fn choose_operation(char op)
{
    return op == '+' ? add : multiply;
}

int main(void)
{
    CLINGS_CHECK_INT(apply_operation(add, 2, 3), 5);
    CLINGS_CHECK_INT(apply_operation(multiply, 2, 3), 6);
    CLINGS_CHECK_INT(choose_operation('+')(4, 5), 9);
    CLINGS_CHECK_INT(choose_operation('*')(4, 5), 20);
    return clings_report();
}
