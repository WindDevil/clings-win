/*
 * clings 练习: 19_modern_c_library/01_noreturn
 * title: _Noreturn 函数
 * objective: 声明一个不会返回的函数，并观察它的退出状态。
 * hint: 子进程带着 "child" 参数重新运行本程序，然后以状态 7 退出。
 */

#include "clings/test.h"

#include <process.h>
#include <stdnoreturn.h>
#include <stdlib.h>
#include <string.h>

_Noreturn void terminate_now(void)
{
    exit(7);
}

int run_noreturn(int argc, char **argv)
{
    if (argc > 1 && strcmp(argv[1], "child") == 0) {
        terminate_now();
    }

    /* Windows 没有 fork()。子进程就是同一个可执行文件， */
    /* 带一个标记参数重新运行，好区分两种角色。 */
    const char *child_args[] = {argv[0], "child", NULL};
    intptr_t child = _spawnv(_P_NOWAIT, argv[0], child_args);
    if (child == -1) {
        return 0;
    }

    int status = 0;
    if (_cwait(&status, child, _WAIT_CHILD) == -1) {
        return 0;
    }
    return status == 7;
}

int main(int argc, char **argv)
{
    CLINGS_CHECK_INT(run_noreturn(argc, argv), 1);
    return clings_report();
}
