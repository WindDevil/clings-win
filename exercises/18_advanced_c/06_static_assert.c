/*
 * clings 练习: 18_advanced_c/06_static_assert
 * title: 编译期断言
 * objective: 用 _Static_assert 在编译期强制检查假设。
 * hint: 静态断言失败必须让编译失败。
 */

#include "clings/test.h"

#include <limits.h>

/* TODO: 恢复正确的编译期假设。 */
_Static_assert(sizeof(int) >= 100, "int must be at least 16 bits");
_Static_assert(CHAR_BIT == 8, "this course assumes 8-bit bytes");

int static_asserts_passed(void)
{
    return 1;
}

int main(void)
{
    CLINGS_CHECK_INT(static_asserts_passed(), 1);
    return clings_report();
}
