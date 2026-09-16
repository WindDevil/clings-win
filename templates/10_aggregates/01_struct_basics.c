/*
 * clings exercise: 10_aggregates/01_struct_basics
 * title: Defining and using structs
 * objective: Create a struct value and access its members through a pointer.
 * hint: Use the arrow operator when you have a pointer.
 */

#include "clings/test.h"

struct point {
    int x;
    int y;
};

struct point make_point(int x, int y)
{
    struct point point = {x, y};
    return point;
}

int point_sum(const struct point *point)
{
    /* TODO: return the sum of both coordinates. */
    return point->x - point->y;
}

int main(void)
{
    struct point point = make_point(3, 4);

    CLINGS_CHECK_INT(point.x, 3);
    CLINGS_CHECK_INT(point.y, 4);
    CLINGS_CHECK_INT(point_sum(&point), 7);
    return clings_report();
}
