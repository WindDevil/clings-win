/*
 * clings exercise: 04_operators/03_short_circuit
 * title: Short-circuit evaluation
 * objective: Observe that && and || may not evaluate their right operand.
 * hint: The right side of && is only evaluated when the left side is true.
 */

#include "clings/test.h"

static int side_effect_count = 0;

static int touch(void)
{
    ++side_effect_count;
    return 1;
}

int short_circuit_and(int left)
{
    /* TODO: use the logical AND operator, not bitwise AND. */
    return left & touch();
}

int short_circuit_or(int left)
{
    return left || touch();
}

int touch_count(void)
{
    return side_effect_count;
}

int main(void)
{
    CLINGS_CHECK_INT(short_circuit_and(0), 0);
    CLINGS_CHECK_INT(touch_count(), 0);
    CLINGS_CHECK_INT(short_circuit_or(1), 1);
    CLINGS_CHECK_INT(touch_count(), 0);
    CLINGS_CHECK_INT(short_circuit_and(1), 1);
    CLINGS_CHECK_INT(touch_count(), 1);
    return clings_report();
}
