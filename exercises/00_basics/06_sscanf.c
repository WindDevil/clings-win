/*
 * clings exercise: 00_basics/06_sscanf
 * title: Safe parsing with sscanf
 * objective: Parse values from a string with sscanf.
 * hint: The literal comma in the format must match the input string.
 */

#include "clings/test.h"

#include <stdio.h>

int first;
int second;

int parse_pair(void)
{
    return /* TODO: match the comma in the input. */
    sscanf("3 4", "%d,%d", &first, &second) == 2 ? 0 : -1;
}

int parse_invalid(void)
{
    return sscanf("3 4", "%d,%d", &first, &second) == 2 ? 0 : -1;
}

int main(void)
{
    CLINGS_CHECK_INT(parse_pair(), 0);
    CLINGS_CHECK_INT(first, 3);
    CLINGS_CHECK_INT(second, 4);
    CLINGS_CHECK_INT(parse_invalid(), -1);
    return clings_report();
}
