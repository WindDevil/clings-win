/*
 * clings exercise: 04_operators/06_sizeof_incdec
 * title: sizeof and increment operators
 * objective: Distinguish sizeof expressions from increment side effects.
 * hint: Post-increment returns the old value; pre-increment returns the new value.
 */

#include "clings/test.h"

int size_of_char(void)
{
    return (int)sizeof(char);
}

int post_increment(int *value)
{
    return (*value)++;
}

int pre_increment(int *value)
{
    return ++(*value);
}

int main(void)
{
    int value = 5;

    CLINGS_CHECK_INT(size_of_char(), 1);
    CLINGS_CHECK_INT(post_increment(&value), 5);
    CLINGS_CHECK_INT(value, 6);
    CLINGS_CHECK_INT(pre_increment(&value), 7);
    CLINGS_CHECK_INT(value, 7);
    return clings_report();
}
