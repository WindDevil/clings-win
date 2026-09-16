/*
 * clings 练习: 17_translation_units/01_header_source_split
 * title: 头文件与源文件分离
 * objective: 用 main 文件、头文件和实现文件编译一个程序。
 * hint: 在头文件里声明 add，在 math_utils.c 里定义它。
 */

#include "clings/test.h"
#include "math_utils.h"

int main(void)
{
    CLINGS_CHECK_INT(add(2, 3), 5);
    CLINGS_CHECK_INT(add(-4, 4), 0);
    return clings_report();
}
