/*
 * clings exercise: 18_advanced_c/03_pthreads
 * title: POSIX threads and a mutex
 * objective: Create threads and protect shared state with a mutex.
 * hint: Each worker increments the shared counter 1000 times.
 */

#include "clings/test.h"

#include <pthread.h>

struct counter {
    long value;
};

static pthread_mutex_t counter_mutex = PTHREAD_MUTEX_INITIALIZER;

static void *worker(void *argument)
{
    struct counter *counter = argument;
    for (int i = 0; i < 1000; ++i) {
        pthread_mutex_lock(&counter_mutex);
        /* TODO: increment the shared counter. */
        counter->value += 0;
        pthread_mutex_unlock(&counter_mutex);
    }
    return NULL;
}

int run_threads(void)
{
    struct counter counter = {0};
    pthread_t first;
    pthread_t second;

    if (pthread_create(&first, NULL, worker, &counter) != 0) {
        return -1;
    }
    if (pthread_create(&second, NULL, worker, &counter) != 0) {
        pthread_join(first, NULL);
        return -1;
    }

    pthread_join(first, NULL);
    pthread_join(second, NULL);
    return (int)counter.value;
}

int main(void)
{
    CLINGS_CHECK_INT(run_threads(), 2000);
    return clings_report();
}
