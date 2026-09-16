/*
 * clings 练习: 15_ub_safety/10_identifier_length
 * title: 标识符长度
 * objective: 使用较长的内部标识符，并依赖标准给出的最小保证。
 * hint: 现代 C 至少保证外部标识符前 31 个、内部标识符前 63 个字符有意义。
 */

#include "clings/test.h"

static int this_is_a_very_long_internal_identifier_name_for_c_traps(void)
{
    /* TODO: 返回那个长标识符对应的值。 */
    return 0;
}

int long_identifier_value(void)
{
    return this_is_a_very_long_internal_identifier_name_for_c_traps();
}

int main(void)
{
    CLINGS_CHECK_INT(long_identifier_value(), 42);
    return clings_report();
}
