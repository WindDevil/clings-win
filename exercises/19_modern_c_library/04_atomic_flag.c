/*
 * clings 练习: 19_modern_c_library/04_atomic_flag
 * title: atomic_flag 自旋锁
 * objective: 用 atomic_flag 实现一个简单的测试并设置锁。
 * hint: atomic_flag_test_and_set 返回之前的状态。
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
    /* TODO: 释放锁。 */
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
