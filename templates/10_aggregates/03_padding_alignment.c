/*
 * clings exercise: 10_aggregates/03_padding_alignment
 * title: Padding and alignment
 * objective: Observe padding and member offsets with offsetof.
 * hint: offsetof takes the struct type and the member name.
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
    /* TODO: measure the offset of the value member. */
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
