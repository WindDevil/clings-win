/*
 * clings exercise: 06_functions/07_main_return_value
 * title: main return values
 * objective: Return a defined success or failure status from a program.
 * hint: Return 0 for success and 1 for failure.
 */

#include "clings/test.h"

int exit_code_for(int success)
{
    return success ? 0 : 1;
}

int main(void)
{
    CLINGS_CHECK_INT(exit_code_for(1), 0);
    CLINGS_CHECK_INT(exit_code_for(0), 1);
    return clings_report();
}
