/*
 * clings exercise: 19_modern_c_library/03_atexit
 * title: Registering atexit handlers
 * objective: Register a cleanup function with atexit.
 * hint: atexit returns 0 on success and nonzero on failure.
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
