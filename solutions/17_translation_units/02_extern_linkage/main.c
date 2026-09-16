/*
 * clings exercise: 17_translation_units/02_extern_linkage
 * title: External linkage across files
 * objective: Declare a global variable in a header and define it in another file.
 * hint: The extern declaration promises a definition in config.c.
 */

#include "clings/test.h"
#include "config.h"

int main(void)
{
    CLINGS_CHECK_INT(config_value, 42);
    return clings_report();
}
