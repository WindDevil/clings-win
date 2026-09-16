/*
 * clings exercise: 15_ub_safety/10_identifier_length
 * title: Identifier length
 * objective: Use long internal identifiers and rely on the standard minimum.
 * hint: Modern C guarantees at least 31 significant external and 63 internal identifier characters.
 */

#include "clings/test.h"

static int this_is_a_very_long_internal_identifier_name_for_c_traps(void)
{
    return 42;
}

int long_identifier_value(void)
{
    return this_is_a_very_long_internal_identifier_name_for_c_traps();
}

int main(void)
{
    CLINGS_CHECK_INT(long_identifier_value(), 42);
    return clings_report();
}
