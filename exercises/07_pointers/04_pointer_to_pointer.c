/*
 * clings 练习: 07_pointers/04_pointer_to_pointer
 * title: 指向指针的指针
 * objective: 让函数分配内存并更新调用方持有的指针。
 * hint: 要通过 *slot 赋值，而不是给本地的 slot 参数赋值。
 */

#include "clings/test.h"

#include <stdlib.h>

int allocate_int(int **out, int value)
{
    *out = malloc(sizeof **out);
    if (*out == NULL) {
        return -1;
    }
    **out = value;
    return 0;
}

void set_pointer(int **slot, int *value)
{
    /* TODO: 更新 slot 指向的那个指针。 */
    slot = &value;
}

int main(void)
{
    int *allocated = NULL;
    int value = 5;
    int *slot = NULL;

    CLINGS_CHECK_INT(allocate_int(&allocated, 99), 0);
    CLINGS_CHECK(allocated != NULL);
    CLINGS_CHECK_INT(*allocated, 99);
    free(allocated);
    set_pointer(&slot, &value);
    CLINGS_CHECK(slot == &value);
    return clings_report();
}
