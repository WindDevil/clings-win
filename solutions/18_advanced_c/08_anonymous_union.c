/*
 * clings 练习: 18_advanced_c/08_anonymous_union
 * title: 匿名结构体与联合体
 * objective: 通过外层结构体直接访问匿名联合体的成员。
 * hint: 匿名联合体的成员会提升到外层结构体的作用域里。
 */

#include "clings/test.h"

struct variant {
    int kind;
    union {
        int integer;
        double real;
    };
};

int variant_integer(const struct variant *value)
{
    return value->integer;
}

double variant_real(const struct variant *value)
{
    return value->real;
}

int main(void)
{
    struct variant integer_value = {0};
    struct variant real_value = {0};

    integer_value.kind = 1;
    integer_value.integer = 42;
    CLINGS_CHECK_INT(variant_integer(&integer_value), 42);
    real_value.real = 3.5;
    CLINGS_CHECK_INT(variant_real(&real_value) == 3.5, 1);
    return clings_report();
}
