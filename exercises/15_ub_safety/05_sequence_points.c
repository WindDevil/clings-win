/*
 * clings exercise: 15_ub_safety/05_sequence_points
 * title: Sequence points
 * objective: Avoid unsequenced reads and writes of the same object.
 * hint: Read the old value, update the object, then return the old value.
 */

#include "clings/test.h"

int next_value(int *value)
{
    /* TODO: do not read and modify the same object without a sequence point. */
    return (*value)++ + *value;
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
