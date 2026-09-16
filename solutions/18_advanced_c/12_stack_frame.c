/*
 * clings exercise: 18_advanced_c/12_stack_frame
 * title: Stack frames
 * objective: Observe that nested function calls use distinct activation records.
 * hint: __builtin_frame_address is a GCC/Clang extension.
 */

#include "clings/test.h"

#include <stddef.h>

static void *inner_frame(void)
{
    return __builtin_frame_address(0);
}

void *outer_frame_difference(void)
{
    void *inner = inner_frame();
    return __builtin_frame_address(0) == inner ? NULL : inner;
}

int main(void)
{
    CLINGS_CHECK(outer_frame_difference() != NULL);
    return clings_report();
}
