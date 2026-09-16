/*
 * clings 练习: 03_types_variables/11_char_signedness
 * title: char 的符号性
 * objective: 符号性重要时，明确使用 signed char 和 unsigned char。
 * hint: char 是否带符号由实现决定；signed char 和 unsigned char 则是明确的。
 */

#include "clings/test.h"

int signed_char_value(signed char value)
{
    /* TODO: 保留有符号的值。 */
    return (int)(unsigned char)value;
}

int unsigned_char_value(unsigned char value)
{
    return value;
}

int main(void)
{
    CLINGS_CHECK_INT(signed_char_value((signed char)0xFF), -1);
    CLINGS_CHECK_INT(unsigned_char_value((unsigned char)0xFF), 255);
    return clings_report();
}
