/*
 * clings 练习: 16_data_structures/stack_adt
 * title: 栈抽象数据类型
 * objective: 用定容量数组实现后进先出的栈。
 * hint: 栈顶就是元素个数减一，push 和 pop 都只动栈顶。
 */

#include "clings/test.h"

#include <stddef.h>

#define STACK_CAPACITY 8

struct stack {
    int values[STACK_CAPACITY];
    size_t count;
};

void stack_init(struct stack *stack)
{
    stack->count = 0;
}

int stack_push(struct stack *stack, int value)
{
    if (stack->count == STACK_CAPACITY) {
        return -1;
    }
    /* TODO: 把新值放到栈顶，再把元素个数加一。 */
    stack->values[stack->count] = value;
    return 0;
}

int stack_pop(struct stack *stack, int *out)
{
    if (stack->count == 0) {
        return -1;
    }
    --stack->count;
    *out = stack->values[stack->count];
    return 0;
}

int stack_peek(const struct stack *stack, int *out)
{
    if (stack->count == 0) {
        return -1;
    }
    *out = stack->values[stack->count - 1];
    return 0;
}

size_t stack_size(const struct stack *stack)
{
    return stack->count;
}

int main(void)
{
    struct stack stack;
    int value = 0;

    stack_init(&stack);
    CLINGS_CHECK_INT(stack_size(&stack), 0);
    CLINGS_CHECK_INT(stack_pop(&stack, &value), -1);
    CLINGS_CHECK_INT(stack_push(&stack, 1), 0);
    CLINGS_CHECK_INT(stack_push(&stack, 2), 0);
    CLINGS_CHECK_INT(stack_push(&stack, 3), 0);
    CLINGS_CHECK_INT(stack_size(&stack), 3);
    CLINGS_CHECK_INT(stack_peek(&stack, &value), 0);
    CLINGS_CHECK_INT(value, 3);
    CLINGS_CHECK_INT(stack_pop(&stack, &value), 0);
    CLINGS_CHECK_INT(value, 3);
    CLINGS_CHECK_INT(stack_pop(&stack, &value), 0);
    CLINGS_CHECK_INT(value, 2);
    CLINGS_CHECK_INT(stack_size(&stack), 1);
    return clings_report();
}
