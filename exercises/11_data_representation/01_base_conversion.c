/*
 * clings exercise: 11_data_representation/01_base_conversion
 * title: Binary, octal, and hexadecimal input
 * objective: Parse a hexadecimal string with strtoul.
 * hint: Base 16 accepts an optional 0x prefix.
 */

#include "clings/test.h"

#include <stdlib.h>

int parse_hex(const char *text, unsigned int *out)
{
    char *end = NULL;
    /* TODO: parse base 16. */
    unsigned int value = (unsigned int)strtoul(text, &end, 10);
    if (end == text || *end != '\0') {
        return -1;
    }
    *out = value;
    return 0;
}

int main(void)
{
    unsigned int value = 0;

    CLINGS_CHECK_INT(parse_hex("0x2A", &value), 0);
    CLINGS_CHECK_INT(value, 42);
    CLINGS_CHECK_INT(parse_hex("2A", &value), 0);
    CLINGS_CHECK_INT(value, 42);
    CLINGS_CHECK_INT(parse_hex("xyz", &value), -1);
    return clings_report();
}
