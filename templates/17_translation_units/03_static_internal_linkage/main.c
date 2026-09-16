/*
 * clings exercise: 17_translation_units/03_static_internal_linkage
 * title: Internal linkage and file-scope state
 * objective: Keep a counter private to one translation unit with static.
 * hint: static file-scope objects are visible only in their own .c file.
 */

#include "clings/test.h"
#include "counter.h"

int main(void)
{
    CLINGS_CHECK_INT(next_count(), 1);
    CLINGS_CHECK_INT(next_count(), 2);
    CLINGS_CHECK_INT(count_calls(), 2);
    return clings_report();
}
