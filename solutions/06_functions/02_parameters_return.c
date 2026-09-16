/*
 * clings exercise: 06_functions/02_parameters_return
 * title: Parameters and return values
 * objective: Return values through parameters and clamp a range.
 * hint: When count is zero, leave the outputs unchanged.
 */

#include "clings/test.h"

int clamp(int value, int low, int high)
{
    if (value < low) {
        return low;
    }
    if (value > high) {
        return high;
    }
    return value;
}

int min_of_three(int a, int b, int c)
{
    int minimum = a;
    if (b < minimum) {
        minimum = b;
    }
    if (c < minimum) {
        minimum = c;
    }
    return minimum;
}

int max_of_three(int a, int b, int c)
{
    int maximum = a;
    if (b > maximum) {
        maximum = b;
    }
    if (c > maximum) {
        maximum = c;
    }
    return maximum;
}

int main(void)
{
    CLINGS_CHECK_INT(clamp(5, 1, 10), 5);
    CLINGS_CHECK_INT(clamp(0, 1, 10), 1);
    CLINGS_CHECK_INT(clamp(11, 1, 10), 10);
    CLINGS_CHECK_INT(min_of_three(4, -2, 9), -2);
    CLINGS_CHECK_INT(max_of_three(4, -2, 9), 9);
    return clings_report();
}
