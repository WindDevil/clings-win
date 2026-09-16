/*
 * clings 练习: 19_modern_c_library/03_atexit
 * title: 注册 atexit 处理函数
 * objective: 用 atexit 注册清理函数。
 * hint: atexit 成功返回 0，失败返回非零值。
 */

#include "clings/test.h"

#include <stdlib.h>

static void cleanup(void)
{
}

int register_cleanup(void)
{
    return atexit(cleanup) == 0 ? 0 : -1;
}

int main(void)
{
    CLINGS_CHECK_INT(register_cleanup(), 0);
    return clings_report();
}
