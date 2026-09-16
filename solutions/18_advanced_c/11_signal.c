/*
 * clings exercise: 18_advanced_c/11_signal
 * title: Signals and sig_atomic_t
 * objective: Install a signal handler and use a sig_atomic_t flag.
 * hint: raise(SIGINT) invokes the installed handler synchronously.
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
