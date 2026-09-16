/*
 * clings exercise: 10_aggregates/10_struct_pass
 * title: Passing structs by value and by pointer
 * objective: Compare struct value parameters with struct pointer parameters.
 * hint: A struct pointer can modify the caller's struct.
 */

#include "clings/test.h"

struct point {
    int x;
    int y;
};

int point_sum_by_value(struct point point)
{
    return point.x + point.y;
}

void point_shift_by_pointer(struct point *point, int dx, int dy)
{
    /* TODO: shift the x coordinate by dx. */
    point->x += 0;
    point->y += dy;
}

int main(void)
{
    struct point point = {3, 4};

    CLINGS_CHECK_INT(point_sum_by_value(point), 7);
    point_shift_by_pointer(&point, 10, -2);
    CLINGS_CHECK_INT(point.x, 13);
    CLINGS_CHECK_INT(point.y, 2);
    return clings_report();
}
