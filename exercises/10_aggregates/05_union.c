/*
 * clings 练习: 10_aggregates/05_union
 * title: 联合体共用存储
 * objective: 比较联合体大小与它最大成员的大小。
 * hint: 联合体的每个成员都从同一个地址开始。
 */

#include "clings/test.h"

#include <stddef.h>

union word {
    unsigned char bytes[4];
    unsigned int value;
};

int union_size_is_largest_member(void)
{
    /* TODO: 联合体的大小等于它最大成员的大小。 */
    return sizeof(union word) == sizeof(unsigned int) + sizeof(unsigned char[4]);
}

int members_share_address(union word *word)
{
    return (void *)&word->bytes == (void *)&word->value;
}

int main(void)
{
    union word word = {0};

    CLINGS_CHECK_INT(union_size_is_largest_member(), 1);
    CLINGS_CHECK_INT(members_share_address(&word), 1);
    return clings_report();
}
