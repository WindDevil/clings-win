/*
 * clings exercise: 19_modern_c_library/04_atomic_flag
 * title: atomic_flag spin lock
 * objective: Use atomic_flag as a simple test-and-set lock.
 * hint: atomic_flag_test_and_set returns the previous state.
 */

#include "clings/test.h"

#include <stdatomic.h>

static atomic_flag lock = ATOMIC_FLAG_INIT;

int try_lock_flag(void)
{
    return !atomic_flag_test_and_set(&lock);
}

void unlock_flag(void)
{
    /* TODO: release the lock. */
}

int main(void)
{
    CLINGS_CHECK_INT(try_lock_flag(), 1);
    CLINGS_CHECK_INT(try_lock_flag(), 0);
    unlock_flag();
    CLINGS_CHECK_INT(try_lock_flag(), 1);
    unlock_flag();
    return clings_report();
}
