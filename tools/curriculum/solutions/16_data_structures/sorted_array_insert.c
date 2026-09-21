/*
 * clings 练习: 16_data_structures/sorted_array_insert
 * title: 有序数组的插入与查找
 * objective: 让数组始终保持升序，并按值查找。
 * hint: 插入时从后往前挪元素，给新值腾出位置；数组满了返回 -1。
 */

#include "clings/test.h"

#include <stddef.h>

#define SORTED_CAPACITY 8

struct sorted_array {
    int values[SORTED_CAPACITY];
    size_t count;
};

void sorted_init(struct sorted_array *array)
{
    array->count = 0;
}

int sorted_insert(struct sorted_array *array, int value)
{
    if (array->count == SORTED_CAPACITY) {
        return -1;
    }
    size_t position = 0;
    while (position < array->count && array->values[position] < value) {
        ++position;
    }
    for (size_t index = array->count; index > position; --index) {
        array->values[index] = array->values[index - 1];
    }
    array->values[position] = value;
    ++array->count;
    return 0;
}

int sorted_find(const struct sorted_array *array, int value)
{
    for (size_t index = 0; index < array->count; ++index) {
        if (array->values[index] == value) {
            return (int)index;
        }
    }
    return -1;
}

int main(void)
{
    struct sorted_array array;

    sorted_init(&array);
    CLINGS_CHECK_INT(sorted_insert(&array, 3), 0);
    CLINGS_CHECK_INT(sorted_insert(&array, 1), 0);
    CLINGS_CHECK_INT(sorted_insert(&array, 2), 0);
    CLINGS_CHECK_INT(array.count, 3);
    CLINGS_CHECK_INT(array.values[0], 1);
    CLINGS_CHECK_INT(array.values[1], 2);
    CLINGS_CHECK_INT(array.values[2], 3);
    CLINGS_CHECK_INT(sorted_find(&array, 2), 1);
    CLINGS_CHECK_INT(sorted_find(&array, 4), -1);
    return clings_report();
}
