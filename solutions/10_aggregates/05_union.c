/*
 * clings exercise: 10_aggregates/05_union
 * title: Unions share storage
 * objective: Compare union size with the size of its largest member.
 * hint: Every union member starts at the same address.
 */

#include "clings/test.h"

#include <stddef.h>

union word {
    unsigned char bytes[4];
    unsigned int value;
};

int union_size_is_largest_member(void)
{
    return sizeof(union word) == sizeof(unsigned int);
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
