/*
 * clings exercise: 05_control_flow/06_semicolon_pitfalls
 * title: Semicolon and empty-statement traps
 * objective: Avoid accidentally ending an if or loop with a semicolon.
 * hint: A semicolon after if creates an empty body.
 */

#include "clings/test.h"

int count_nonzero(const int *values, int count)
{
    int nonzero = 0;
    for (int i = 0; i < count; ++i) {
        if (values[i] != 0) {
            ++nonzero;
        }
    }
    return nonzero;
}

int main(void)
{
    const int values[] = {0, 1, 2};
    const int zeros[] = {0, 0, 0};

    CLINGS_CHECK_INT(count_nonzero(values, 3), 2);
    CLINGS_CHECK_INT(count_nonzero(zeros, 3), 0);
    return clings_report();
}
