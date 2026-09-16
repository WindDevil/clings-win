/*
 * clings 练习: 08_arrays_strings/08_compound_literals
 * title: 复合字面量
 * objective: 用复合字面量创建临时结构体值。
 * hint: 写法是 (struct point){.x = 3, .y = 4}。
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
