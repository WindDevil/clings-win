/*
 * clings exercise: 16_data_structures/01_queue_adt
 * title: Queue ADT
 * objective: Implement a fixed-capacity circular queue.
 * hint: The tail index wraps with modulo capacity.
 */

#include "clings/test.h"

#include <stddef.h>

#define QUEUE_CAPACITY 8

struct queue {
    int values[QUEUE_CAPACITY];
    size_t head;
    size_t tail;
    size_t count;
};

void queue_init(struct queue *queue)
{
    queue->head = 0;
    queue->tail = 0;
    queue->count = 0;
}

int queue_push(struct queue *queue, int value)
{
    if (queue->count == QUEUE_CAPACITY) {
        return -1;
    }
    /* TODO: store the new value. */
    queue->values[queue->tail] = 0;
    queue->tail = (queue->tail + 1) % QUEUE_CAPACITY;
    ++queue->count;
    return 0;
}

int queue_pop(struct queue *queue, int *out)
{
    if (queue->count == 0) {
        return -1;
    }
    *out = queue->values[queue->head];
    queue->head = (queue->head + 1) % QUEUE_CAPACITY;
    --queue->count;
    return 0;
}

size_t queue_size(const struct queue *queue)
{
    return queue->count;
}

int main(void)
{
    struct queue queue;
    int value = 0;

    queue_init(&queue);
    CLINGS_CHECK_INT(queue_size(&queue), 0);
    CLINGS_CHECK_INT(queue_push(&queue, 1), 0);
    CLINGS_CHECK_INT(queue_push(&queue, 2), 0);
    CLINGS_CHECK_INT(queue_push(&queue, 3), 0);
    CLINGS_CHECK_INT(queue_size(&queue), 3);
    CLINGS_CHECK_INT(queue_pop(&queue, &value), 0);
    CLINGS_CHECK_INT(value, 1);
    CLINGS_CHECK_INT(queue_pop(&queue, &value), 0);
    CLINGS_CHECK_INT(value, 2);
    return clings_report();
}
