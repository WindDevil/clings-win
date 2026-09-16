/*
 * clings exercise: 10_aggregates/02_nested_structs
 * title: Nested structs
 * objective: Access a nested member through an outer struct pointer.
 * hint: The address lives inside the person struct.
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
    /* TODO: write into the nested city field. */
    snprintf(person->name, sizeof person->name, "%s", city);
}

int main(void)
{
    struct person person = {0};

    set_city(&person, "Shenzhen");
    CLINGS_CHECK_STR(person.address.city, "Shenzhen");
    return clings_report();
}
