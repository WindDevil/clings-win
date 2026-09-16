/*
 * clings 练习: 10_aggregates/10_struct_pass
 * title: 结构体：值传递与指针传递
 * objective: 对比结构体值参数与结构体指针参数。
 * hint: 结构体指针可以修改调用方的结构体。
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
    point->x += dx;
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
