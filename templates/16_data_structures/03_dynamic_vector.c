/*
 * clings 练习: 16_data_structures/03_dynamic_vector
 * title: 动态数组（vector）
 * objective: 扩容动态数组，并保留已有元素。
 * hint: 数组满时把容量翻倍。
 */

#include "clings/test.h"

#include <stddef.h>
#include <stdlib.h>

struct vector {
    int *values;
    size_t size;
    size_t capacity;
};

int vector_push(struct vector *vector, int value)
{
    if (vector->size == vector->capacity) {
        size_t new_capacity = vector->capacity == 0 ? 2 : vector->capacity * 2;
        int *grown = realloc(vector->values, new_capacity * sizeof *grown);
        if (grown == NULL) {
            return -1;
        }
        vector->values = grown;
        vector->capacity = new_capacity;
    }
    /* TODO: 追加这个值，并把 size 加一。 */
    vector->values[vector->size] = value;
    return 0;
}

void vector_free(struct vector *vector)
{
    free(vector->values);
    vector->values = NULL;
    vector->size = 0;
    vector->capacity = 0;
}

int main(void)
{
    struct vector vector = {0};

    for (int value = 1; value <= 5; ++value) {
        CLINGS_CHECK_INT(vector_push(&vector, value), 0);
    }
    CLINGS_CHECK_INT(vector.size, 5);
    CLINGS_CHECK_INT(vector.values[0], 1);
    CLINGS_CHECK_INT(vector.values[4], 5);
    vector_free(&vector);
    return clings_report();
}
