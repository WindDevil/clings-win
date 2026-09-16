/*
 * clings exercise: 18_advanced_c/04_atomics
 * title: C11 atomics
 * objective: Use atomic_int for lock-free counter updates.
 * hint: atomic_fetch_add adds to the current value and returns the old value.
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
    /* TODO: add amount to the existing value. */
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
