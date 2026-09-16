/*
 * clings exercise: 03_types_variables/07_qualifiers
 * title: Type qualifiers and storage-class specifiers
 * objective: Use const, volatile, extern, auto, and register.
 * hint: Qualifiers affect how an object may be accessed and optimized.
 */

#include "clings/test.h"

extern int shared_value;
int shared_value = 42;

int const_value(void)
{
    const int value = 42;
    return value;
}

int volatile_value(void)
{
    /* TODO: initialize the volatile value. */
    volatile int value = 0;
    return value;
}

int register_sum(void)
{
    register int sum = 0;
    for (register int i = 0; i < 3; ++i) {
        sum += i;
    }
    return sum;
}

int auto_value(void)
{
    auto int value = 5;
    return value;
}

int main(void)
{
    CLINGS_CHECK_INT(shared_value, 42);
    CLINGS_CHECK_INT(const_value(), 42);
    CLINGS_CHECK_INT(volatile_value(), 7);
    CLINGS_CHECK_INT(register_sum(), 3);
    CLINGS_CHECK_INT(auto_value(), 5);
    return clings_report();
}
