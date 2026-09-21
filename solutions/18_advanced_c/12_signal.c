/*
 * clings 练习: 18_advanced_c/12_signal
 * title: 信号与 sig_atomic_t
 * objective: 安装信号处理函数，并使用 sig_atomic_t 标志。
 * hint: raise(SIGINT) 会同步调用已经安装的处理函数。
 */

#include "clings/test.h"

#include <signal.h>

static volatile sig_atomic_t caught = 0;

static void handle_signal(int signal_number)
{
    (void)signal_number;
    caught = 1;
}

int raise_and_catch(void)
{
    caught = 0;
    if (signal(SIGINT, handle_signal) == SIG_ERR) {
        return -1;
    }
    if (raise(SIGINT) != 0) {
        return -1;
    }
    return caught ? 0 : -1;
}

int main(void)
{
    CLINGS_CHECK_INT(raise_and_catch(), 0);
    return clings_report();
}
