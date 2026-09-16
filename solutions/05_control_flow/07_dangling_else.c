/*
 * clings exercise: 05_control_flow/07_dangling_else
 * title: Dangling else
 * objective: Use braces to make else bind to the intended if.
 * hint: Without braces, else binds to the nearest unmatched if.
 */

#include "clings/test.h"

int classify(int x, int y)
{
    if (x > 0) {
        if (y > 0) {
            return 1;
        }
    } else {
        return 2;
    }
    return 0;
}

int main(void)
{
    CLINGS_CHECK_INT(classify(1, 1), 1);
    CLINGS_CHECK_INT(classify(1, -1), 0);
    CLINGS_CHECK_INT(classify(-1, 1), 2);
    return clings_report();
}
