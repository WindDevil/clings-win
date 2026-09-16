/*
 * clings exercise: 10_aggregates/07_typedef_designated
 * title: typedef and designated initializers
 * objective: Use a typedef and initialize members by name.
 * hint: Designated initializers make the field mapping explicit.
 */

#include "clings/test.h"

typedef struct {
    int x;
    int y;
} point_t;

point_t make_point(int x, int y)
{
    point_t point = {.x = x, .y = y};
    return point;
}

int main(void)
{
    point_t point = make_point(3, 4);

    CLINGS_CHECK_INT(point.x, 3);
    CLINGS_CHECK_INT(point.y, 4);
    return clings_report();
}
