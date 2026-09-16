/*
 * clings 练习: 03_types_variables/01_integer_types
 * title: 整数类型与取值范围
 * objective: 正确使用 sizeof、CHAR_BIT、INT_MIN 和 INT_MAX。
 * hint: int 的位数是 sizeof(int) * CHAR_BIT。
 */

#include "clings/test.h"

#include <limits.h>

int int_bits(void)
{
    /* TODO: 量的是 int 的宽度，不是 char 的。 */
    return (int)(sizeof(char) * CHAR_BIT);
}

int long_can_hold_int(long value)
{
    return value >= INT_MIN && value <= INT_MAX;
}

int main(void)
{
    CLINGS_CHECK(int_bits() >= 16);
    CLINGS_CHECK_INT(long_can_hold_int(0), 1);
    CLINGS_CHECK_INT(long_can_hold_int((long)INT_MAX), 1);
    {
        /* 平台的数据模型不一样：LP64（Linux）的 long 能装下 INT_MAX，
         * 而 LLP64（Windows）的 long 只有 32 位，装不下。
         * 只有 long 真的比 int 宽，才谈得上 long 型的 INT_MAX + 1。 */
        long above_int_max = (long)INT_MAX;
        if (sizeof(long) > sizeof(int)) {
            CLINGS_CHECK_INT(long_can_hold_int(above_int_max + 1), 0);
        } else {
            CLINGS_CHECK_MSG(sizeof(long) == sizeof(int),
                             "long is not wider than int here");
        }
    }
    return clings_report();
}
