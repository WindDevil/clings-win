/*
 * clings 练习: 06_functions/07_main_return_value
 * title: main 的返回值
 * objective: 让程序返回明确表示成功或失败的状态码。
 * hint: 成功返回 0，失败返回 1。
 */

#include "clings/test.h"

int exit_code_for(int success)
{
    return success ? 0 : 1;
}

int main(void)
{
    CLINGS_CHECK_INT(exit_code_for(1), 0);
    CLINGS_CHECK_INT(exit_code_for(0), 1);
    return clings_report();
}
