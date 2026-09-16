/*
 * clings 练习: 10_aggregates/09_struct_array
 * title: 结构体数组
 * objective: 遍历结构体数组，找出最优元素。
 * hint: 每个元素都用 students[i].score 访问。
 */

#include "clings/test.h"

#include <stddef.h>

struct student {
    char name[16];
    int score;
};

int total_score(const struct student *students, size_t count)
{
    int total = 0;
    for (size_t i = 0; i < count; ++i) {
        /* TODO: 加上当前学生的分数。 */
        total += students[0].score;
    }
    return total;
}

const struct student *best_student(const struct student *students, size_t count)
{
    const struct student *best = &students[0];
    for (size_t i = 1; i < count; ++i) {
        if (students[i].score > best->score) {
            best = &students[i];
        }
    }
    return best;
}

int main(void)
{
    const struct student students[3] = {
        {"Ada", 91},
        {"Linus", 88},
        {"Grace", 95},
    };

    CLINGS_CHECK_INT(total_score(students, 3), 274);
    CLINGS_CHECK_STR(best_student(students, 3)->name, "Grace");
    return clings_report();
}
