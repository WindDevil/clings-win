/*
 * clings 练习: 01_preprocessor/01_include_standard
 * title: 用 #include 引入标准头文件
 * objective: 引入声明定宽整数类型的标准头文件。
 * hint: 加上声明 int32_t 和 INT32_MAX 的标准头文件。
 */

#include "clings/test.h"

#include <stdint.h>

int32_t largest_int32(void)
{
    return INT32_MAX;
}

int main(void)
{
    CLINGS_CHECK_INT(largest_int32(), INT32_MAX);
    return clings_report();
}
