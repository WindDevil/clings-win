/*
 * clings 练习: 01_preprocessor/02_include_user
 * title: 用 #include 引入自己的头文件
 * objective: 引入本地头文件，让其中的宏可见。
 * hint: 在 main.c 里加上对 config.h 的 include。
 */

#include "clings/test.h"
/* TODO: 引入定义 CONFIG_VALUE 的本地头文件。 */

int main(void)
{
    CLINGS_CHECK_INT(CONFIG_VALUE, 42);
    return clings_report();
}
