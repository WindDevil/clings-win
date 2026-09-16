/*
 * clings 练习: 10_aggregates/02_nested_structs
 * title: 嵌套结构体
 * objective: 通过外层结构体指针访问嵌套成员。
 * hint: 这个地址位于 person 结构体内部。
 */

#include "clings/test.h"

#include <stdio.h>

struct address {
    char city[32];
    int zip;
};

struct person {
    char name[32];
    struct address address;
};

void set_city(struct person *person, const char *city)
{
    /* TODO: 写进嵌套的 city 字段。 */
    snprintf(person->name, sizeof person->name, "%s", city);
}

int main(void)
{
    struct person person = {0};

    set_city(&person, "Shenzhen");
    CLINGS_CHECK_STR(person.address.city, "Shenzhen");
    return clings_report();
}
