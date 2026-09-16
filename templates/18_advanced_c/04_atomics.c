/*
 * clings 练习: 18_advanced_c/04_atomics
 * title: C11 原子操作
 * objective: 用 atomic_int 做无锁的计数更新。
 * hint: atomic_fetch_add 把当前值加上去，并返回旧值。
 */

#include "clings/test.h"

#include <stdatomic.h>

struct atomic_counter {
    atomic_int value;
};

void atomic_counter_init(struct atomic_counter *counter)
{
    atomic_init(&counter->value, 0);
}

void atomic_counter_add(struct atomic_counter *counter, int amount)
{
    /* TODO: 把 amount 加到已有的值上。 */
    atomic_store(&counter->value, amount);
}

int atomic_counter_get(const struct atomic_counter *counter)
{
    return atomic_load(&counter->value);
}

int main(void)
{
    struct atomic_counter counter;

    atomic_counter_init(&counter);
    atomic_counter_add(&counter, 5);
    CLINGS_CHECK_INT(atomic_counter_get(&counter), 5);
    atomic_counter_add(&counter, 3);
    CLINGS_CHECK_INT(atomic_counter_get(&counter), 8);
    return clings_report();
}
