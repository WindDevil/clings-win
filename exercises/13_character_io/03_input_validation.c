/*
 * clings exercise: 13_character_io/03_input_validation
 * title: Input validation
 * objective: Reject input with trailing characters or out-of-range values.
 * hint: Use %c after %d to detect trailing non-whitespace input.
 */

#include "clings/test.h"

#include <stdio.h>

int read_choice(const char *input, int *choice)
{
    int value = 0;
    char extra = '\0';
    /* TODO: reject trailing characters. */
    if (sscanf(input, "%d", &value) != 1) {
        return -1;
    }
    if (value < 1 || value > 3) {
        return -1;
    }
    *choice = value;
    return 0;
}

int main(void)
{
    int choice = 0;

    CLINGS_CHECK_INT(read_choice("2", &choice), 0);
    CLINGS_CHECK_INT(choice, 2);
    CLINGS_CHECK_INT(read_choice("2x", &choice), -1);
    CLINGS_CHECK_INT(read_choice("9", &choice), -1);
    CLINGS_CHECK_INT(read_choice("abc", &choice), -1);
    return clings_report();
}
