/*
 * clings 练习: 17_translation_units/02_extern_linkage
 * title: 跨文件的外部链接
 * objective: 在头文件里声明全局变量，在另一个文件里定义它。
 * hint: extern 声明承诺了在 config.c 里有对应的定义。
 */

#include "clings/test.h"
#include "config.h"

int main(void)
{
    CLINGS_CHECK_INT(config_value, 42);
    return clings_report();
}
