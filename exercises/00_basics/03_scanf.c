/*
 * clings exercise: 00_basics/03_scanf
 * title: Read with scanf
 * objective: Read an integer from stdin with scanf.
 * hint: scanf needs the address of the variable: &value.
 */

#include "clings/test.h"

#include <stdio.h>

int read_number(void)
{
    int value = 0;
    /* TODO: scanf needs the address of value. */
    if (scanf("%d", value) != 1) {
        return -1;
    }
    return value;
}

int main(void)
{
    const char *valid_path = "/tmp/clings_scanf_valid.txt";
    const char *invalid_path = "/tmp/clings_scanf_invalid.txt";

    FILE *file = fopen(valid_path, "w");
    CLINGS_CHECK(file != NULL);
    fputs("42", file);
    fclose(file);
    CLINGS_CHECK(freopen(valid_path, "r", stdin) != NULL);
    CLINGS_CHECK_INT(read_number(), 42);

    file = fopen(invalid_path, "w");
    CLINGS_CHECK(file != NULL);
    fputs("abc", file);
    fclose(file);
    CLINGS_CHECK(freopen(invalid_path, "r", stdin) != NULL);
    CLINGS_CHECK_INT(read_number(), -1);

    remove(valid_path);
    remove(invalid_path);
    return clings_report();
}
