/*
 * clings 练习: 10_aggregates/07_typedef_designated
 * title: typedef 与指定初始化器
 * objective: 使用 typedef，并按名字初始化成员。
 * hint: 指定初始化器能把字段对应关系写明确。
 */

#include "clings/test.h"

typedef struct {
    int x;
    int y;
} point_t;

point_t make_point(int x, int y)
{
    /* TODO: 按名字初始化两个成员。 */
    point_t point = {.x = x, .y = 0};
    return point;
}

int main(void)
{
    point_t point = make_point(3, 4);

    CLINGS_CHECK_INT(point.x, 3);
    CLINGS_CHECK_INT(point.y, 4);
    return clings_report();
}
