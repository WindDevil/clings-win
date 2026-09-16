/*
 * clings 练习: 18_advanced_c/09_thread_local
 * title: 线程局部存储
 * objective: 用 _Thread_local 让每个线程拥有自己的对象。
 * hint: 工作线程修改的是它自己那份 thread_value。
 */

#include "clings/test.h"

#include <pthread.h>

/* TODO: 把 thread_value 变成线程局部的。 */
static int thread_value = 0;

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
