/*
 * clings 练习: 18_advanced_c/13_stack_frame
 * title: 栈帧
 * objective: 观察嵌套函数调用使用各自独立的活动记录。
 * hint: __builtin_frame_address 是 GCC/Clang 的扩展。
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
    /* TODO: 返回一个不同的内层栈帧。 */
    return NULL;
}

int main(void)
{
    CLINGS_CHECK(outer_frame_difference() != NULL);
    return clings_report();
}
