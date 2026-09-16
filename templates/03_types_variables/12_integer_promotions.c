/*
 * clings 练习: 03_types_variables/12_integer_promotions
 * title: 整型提升
 * objective: 看清 char 操作数在算术表达式里会提升为 int。
 * hint: 操作数是 char 时，sizeof(left + right) 等于 sizeof(int)。
 */

#include "clings/test.h"

#include <stddef.h>

int char_addition_is_int(void)
{
    char left = 1;
    char right = 2;
    /* TODO: 求和的结果会提升为 int。 */
    return sizeof(left + right) == sizeof(char);
}

int unsigned_char_promotion(void)
{
    unsigned char value = 255;
    return (int)value + 1;
}

int main(void)
{
    CLINGS_CHECK_INT(char_addition_is_int(), 1);
    CLINGS_CHECK_INT(unsigned_char_promotion(), 256);
    return clings_report();
}
