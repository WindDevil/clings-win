/*
 * clings exercise: 15_ub_safety/05_sequence_points
 * title: Sequence points
 * objective: Avoid unsequenced reads and writes of the same object.
 * hint: Read the old value, update the object, then return the old value.
 */

#include "clings/test.h"

int next_value(int *value)
{
    int current = *value;
    *value = current + 1;
    return current;
}

int main(void)
{
    int value = 5;

    CLINGS_CHECK_INT(next_value(&value), 5);
    CLINGS_CHECK_INT(value, 6);
    CLINGS_CHECK_INT(next_value(&value), 6);
    CLINGS_CHECK_INT(value, 7);
    return clings_report();
}
