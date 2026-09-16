/*
 * clings exercise: 10_aggregates/12_complex_declarations
 * title: Complex declarations and function-pointer tables
 * objective: Read and use a typedef for a function pointer and an array of function pointers.
 * hint: binary_operation is a typedef for int (*)(int, int).
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
    /* TODO: call the selected operation. */
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
