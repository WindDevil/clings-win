/*
 * clings exercise: 08_arrays_strings/08_compound_literals
 * title: Compound literals
 * objective: Create a temporary struct value with a compound literal.
 * hint: The syntax is (struct point){.x = 3, .y = 4}.
 */

#include "clings/test.h"

struct point {
    int x;
    int y;
};

int point_sum(struct point point)
{
    return point.x + point.y;
}

int compound_literal_sum(void)
{
    return point_sum((struct point){.x = 3, .y = 4});
}

int main(void)
{
    CLINGS_CHECK_INT(compound_literal_sum(), 7);
    CLINGS_CHECK_INT(point_sum((struct point){1, 2}), 3);
    return clings_report();
}
