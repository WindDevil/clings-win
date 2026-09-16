/*
 * clings exercise: 18_advanced_c/09_thread_local
 * title: Thread-local storage
 * objective: Use _Thread_local to give each thread its own object.
 * hint: The worker thread modifies its own copy of thread_value.
 */

#include "clings/test.h"

#include <pthread.h>

static _Thread_local int thread_value = 0;

static void *worker(void *argument)
{
    (void)argument;
    thread_value = 42;
    return NULL;
}

int thread_local_demo(void)
{
    pthread_t thread;
    thread_value = 7;
    if (pthread_create(&thread, NULL, worker, NULL) != 0) {
        return -1;
    }
    pthread_join(thread, NULL);
    return thread_value;
}

int main(void)
{
    CLINGS_CHECK_INT(thread_local_demo(), 7);
    return clings_report();
}
