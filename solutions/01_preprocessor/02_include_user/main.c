/*
 * clings exercise: 01_preprocessor/02_include_user
 * title: #include with a user header
 * objective: Include a local header so its macro is visible.
 * hint: Add the include for config.h in main.c.
 */

#include "clings/test.h"
#include "config.h"

int main(void)
{
    CLINGS_CHECK_INT(CONFIG_VALUE, 42);
    return clings_report();
}
