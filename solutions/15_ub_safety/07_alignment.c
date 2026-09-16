/*
 * clings 练习: 15_ub_safety/07_alignment
 * title: 对齐要求
 * objective: 用 alignof 查询对齐，并让成员保持对齐。
 * hint: alignof 给出该类型要求的最严格对齐。
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
