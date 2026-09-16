/*
 * clings exercise: 15_ub_safety/07_alignment
 * title: Alignment requirements
 * objective: Query alignment with alignof and keep members aligned.
 * hint: alignof reports the strictest alignment the type requires.
 */

#include "clings/test.h"

#include <stdalign.h>
#include <stddef.h>

struct aligned {
    char first;
    max_align_t second;
};

int align_of_int(void)
{
    return (int)alignof(int);
}

int second_member_is_aligned(void)
{
    return (offsetof(struct aligned, second) % alignof(max_align_t)) == 0;
}

int main(void)
{
    CLINGS_CHECK(align_of_int() >= (int)alignof(short));
    CLINGS_CHECK_INT(second_member_is_aligned(), 1);
    return clings_report();
}
