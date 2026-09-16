/*
 * clings 练习: 00_basics/07_include_header
 * title: 引入 I/O 头文件
 * objective: 引入声明 printf 的标准头文件。
 * hint: 编译器需要 printf 的声明；加上标准 I/O 头文件。
 */

#include "clings/test.h"

/* TODO: 引入声明 printf 的头文件。 */
int print_greeting(void)
{
    return printf("header works\n");
}

int main(void)
{
    CLINGS_CHECK_INT(print_greeting(), 13);
    return clings_report();
}
