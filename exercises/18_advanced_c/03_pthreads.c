/*
 * clings 练习: 18_advanced_c/03_pthreads
 * title: POSIX 线程与互斥量
 * objective: 创建线程，并用互斥量保护共享状态。
 * hint: 每个工作线程把共享计数器加 1000 次。
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
        /* TODO: 递增共享计数器。 */
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
