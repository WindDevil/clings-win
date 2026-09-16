/*
 * clings exercise: 08_arrays_strings/14_fgets_fputs_sort
 * title: fgets, fputs, and sorting strings
 * objective: Read a line with fgets and sort an array of strings.
 * hint: qsort receives an array of pointers, so cast to const char *const *.
 */

#include "clings/test.h"

#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int compare_strings(const void *left, const void *right)
{
    /* TODO: sort in ascending order. */
    return strcmp(*(const char *const *)right, *(const char *const *)left);
}

void sort_strings(const char **values, size_t count)
{
    qsort(values, count, sizeof *values, compare_strings);
}

int read_line(FILE *file, char *buffer, size_t size)
{
    return fgets(buffer, (int)size, file) != NULL ? 0 : -1;
}

int main(void)
{
    FILE *file = tmpfile();
    char buffer[16];
    const char *values[3] = {"pear", "apple", "banana"};

    CLINGS_CHECK(file != NULL);
    fputs("hello\n", file);
    rewind(file);
    CLINGS_CHECK_INT(read_line(file, buffer, sizeof buffer), 0);
    CLINGS_CHECK_STR(buffer, "hello\n");
    fclose(file);
    sort_strings(values, 3);
    CLINGS_CHECK_STR(values[0], "apple");
    CLINGS_CHECK_STR(values[1], "banana");
    CLINGS_CHECK_STR(values[2], "pear");
    return clings_report();
}
