/*
 * clings exercise: 18_advanced_c/08_anonymous_union
 * title: Anonymous structs and unions
 * objective: Access anonymous union members directly through the outer struct.
 * hint: An anonymous union member is promoted into the enclosing struct scope.
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
    /* TODO: read the anonymous union member. */
    return value->kind;
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
