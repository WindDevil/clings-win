/*
 * clings exercise: 07_pointers/13_function_pointers
 * title: Function pointers and dispatch
 * objective: Store functions in variables and choose one at runtime.
 * hint: Return the function that matches the operator character.
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
    /* TODO: choose multiply for any non-plus operator. */
    return add;
}

int main(void)
{
    CLINGS_CHECK_INT(apply_operation(add, 2, 3), 5);
    CLINGS_CHECK_INT(apply_operation(multiply, 2, 3), 6);
    CLINGS_CHECK_INT(choose_operation('+')(4, 5), 9);
    CLINGS_CHECK_INT(choose_operation('*')(4, 5), 20);
    return clings_report();
}
