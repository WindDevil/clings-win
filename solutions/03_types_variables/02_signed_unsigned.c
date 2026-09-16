/*
 * clings 练习: 03_types_variables/02_signed_unsigned
 * title: 有符号与无符号转换
 * objective: 比较时避开寻常算术转换的陷阱。
 * hint: 负的 int 转成无符号后会变成很大的值。
 */

#include "clings/test.h"

int compare_int_unsigned(int a, unsigned b)
{
    if (a < 0) {
        return -1;
    }
    if ((unsigned)a < b) {
        return -1;
    }
    if ((unsigned)a > b) {
        return 1;
    }
    return 0;
}

int main(void)
{
    CLINGS_CHECK_INT(compare_int_unsigned(-1, 0u), -1);
    CLINGS_CHECK_INT(compare_int_unsigned(5, 3u), 1);
    CLINGS_CHECK_INT(compare_int_unsigned(3, 3u), 0);
    CLINGS_CHECK_INT(compare_int_unsigned(2, 9u), -1);
    return clings_report();
}
