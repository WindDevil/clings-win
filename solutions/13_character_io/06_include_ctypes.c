/*
 * clings 练习: 13_character_io/06_include_ctypes
 * title: 引入 ctype.h
 * objective: 先引入声明 toupper 的头文件，再调用它。
 * hint: 编译器需要 ctype.h 里的声明；把这个 include 加上。
 */

#include "clings/test.h"

#include <ctype.h>

int uppercase_a(void)
{
    return toupper('a');
}

int main(void)
{
    CLINGS_CHECK_INT(uppercase_a(), 'A');
    return clings_report();
}
