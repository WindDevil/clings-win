/*
 * clings 练习: 03_types_variables/08_stdbool_stddef
 * title: stdbool.h 与 stddef.h
 * objective: 使用标准头文件里的 bool 和 size_t。
 * hint: bool 定义在 <stdbool.h>；size_t 定义在 <stddef.h>。
 */

#include "clings/test.h"

#include <stdbool.h>
#include <stddef.h>

bool is_even(int value)
{
    /* TODO: 返回 bool 结果，而不是整数余数。 */
    return value % 2;
}

size_t size_of_int(void)
{
    return sizeof(int);
}

int main(void)
{
    CLINGS_CHECK_INT(is_even(4), 1);
    CLINGS_CHECK_INT(is_even(3), 0);
    CLINGS_CHECK_INT(size_of_int(), sizeof(int));
    return clings_report();
}
