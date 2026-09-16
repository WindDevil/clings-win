/*
 * clings 练习: 10_aggregates/03_padding_alignment
 * title: 填充与对齐
 * objective: 用 offsetof 观察填充和成员偏移。
 * hint: offsetof 接收结构体类型和成员名。
 */

#include "clings/test.h"

#include <stddef.h>

struct padded {
    char first;
    int value;
    char last;
};

int value_offset(void)
{
    /* TODO: 测出 value 成员的偏移。 */
    return (int)offsetof(struct padded, first);
}

int padded_size(void)
{
    return (int)sizeof(struct padded);
}

int main(void)
{
    CLINGS_CHECK(value_offset() >= (int)sizeof(char));
    CLINGS_CHECK(padded_size() >= value_offset() + (int)sizeof(int) + 1);
    CLINGS_CHECK_INT((int)sizeof(struct padded) % (int)sizeof(int), 0);
    return clings_report();
}
