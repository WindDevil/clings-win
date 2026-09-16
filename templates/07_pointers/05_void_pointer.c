/*
 * clings 练习: 07_pointers/05_void_pointer
 * title: 通用字节交换
 * objective: 用 void 指针和 unsigned char 写与类型无关的代码。
 * hint: 先把 a 里的字节存下来，再覆盖它。
 */

#include "clings/test.h"

#include <stddef.h>

void swap_bytes(void *left, void *right, size_t size)
{
    unsigned char *a = left;
    unsigned char *b = right;

    for (size_t i = 0; i < size; ++i) {
        unsigned char temporary = a[i];
        a[i] = b[i];
        /* TODO: 完成字节交换。 */
        b[i] = a[i];
    }
}

int main(void)
{
    int a = 0x11223344;
    int b = 0x55667788;
    double x = 1.5;
    double y = 2.5;

    swap_bytes(&a, &b, sizeof a);
    CLINGS_CHECK_INT(a, 0x55667788);
    CLINGS_CHECK_INT(b, 0x11223344);
    swap_bytes(&x, &y, sizeof x);
    CLINGS_CHECK_INT(x == 2.5, 1);
    CLINGS_CHECK_INT(y == 1.5, 1);
    return clings_report();
}
