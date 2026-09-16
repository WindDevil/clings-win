/*
 * clings 练习: 08_arrays_strings/07_vla
 * title: 变长数组
 * objective: 创建长度由运行时决定的数据。
 * hint: 变长数组用运行时表达式声明：int values[n]。
 */

#include "clings/test.h"

int sum_vla(int count)
{
    int values[count];
    for (int i = 0; i < count; ++i) {
        /* TODO: 初始化变长数组的元素。 */
        values[i] = 1;
    }
    int sum = 0;
    for (int i = 0; i < count; ++i) {
        sum += values[i];
    }
    return sum;
}

int main(void)
{
    CLINGS_CHECK_INT(sum_vla(1), 1);
    CLINGS_CHECK_INT(sum_vla(4), 10);
    CLINGS_CHECK_INT(sum_vla(10), 55);
    return clings_report();
}
