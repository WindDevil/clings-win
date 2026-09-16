/*
 * clings 练习: 06_functions/04_static_inline
 * title: 内部链接与内联辅助函数
 * objective: 使用 static 函数和文件作用域状态。
 * hint: 返回自增后的值之前，先更新 call_count。
 */

#include "clings/test.h"

static int call_count = 0;

static int add_one(int value)
{
    /* TODO: 每次调用都计数。 */
    return value + 1;
}

int call_add_one(int value)
{
    return add_one(value);
}

int add_one_calls(void)
{
    return call_count;
}

int main(void)
{
    CLINGS_CHECK_INT(add_one_calls(), 0);
    CLINGS_CHECK_INT(call_add_one(1), 2);
    CLINGS_CHECK_INT(call_add_one(2), 3);
    CLINGS_CHECK_INT(add_one_calls(), 2);
    return clings_report();
}
