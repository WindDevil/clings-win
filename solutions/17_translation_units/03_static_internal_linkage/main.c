/*
 * clings 练习: 17_translation_units/03_static_internal_linkage
 * title: 内部链接与文件作用域状态
 * objective: 用 static 把计数器限制在单个编译单元内。
 * hint: static 的文件作用域对象只在自己的 .c 文件里可见。
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
