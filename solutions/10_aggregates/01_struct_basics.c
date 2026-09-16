/*
 * clings 练习: 10_aggregates/01_struct_basics
 * title: 定义并使用结构体
 * objective: 创建结构体值，并通过指针访问它的成员。
 * hint: 手里是指针时，就用箭头运算符。
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
    return point->x + point->y;
}

int main(void)
{
    struct point point = make_point(3, 4);

    CLINGS_CHECK_INT(point.x, 3);
    CLINGS_CHECK_INT(point.y, 4);
    CLINGS_CHECK_INT(point_sum(&point), 7);
    return clings_report();
}
