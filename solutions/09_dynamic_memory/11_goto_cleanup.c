/*
 * clings exercise: 09_dynamic_memory/11_goto_cleanup
 * title: goto for single-exit cleanup
 * objective: Use goto for a clear cleanup path in C.
 * hint: Set *out only after the copy has been allocated and filled.
 */

#include "clings/test.h"

#include <stdlib.h>

int parse_and_sum(const int *values, int count, int *out)
{
    int *copy = NULL;
    int result = -1;

    if (values == NULL || out == NULL || count < 0) {
        goto cleanup;
    }

    copy = malloc((size_t)count * sizeof *copy);
    if (copy == NULL) {
        goto cleanup;
    }

    for (int i = 0; i < count; ++i) {
        copy[i] = values[i];
    }

    int sum = 0;
    for (int i = 0; i < count; ++i) {
        sum += copy[i];
    }
    *out = sum;
    result = 0;

cleanup:
    free(copy);
    return result;
}

int main(void)
{
    const int values[] = {1, 2, 3, 4};
    int out = 0;

    CLINGS_CHECK_INT(parse_and_sum(values, 4, &out), 0);
    CLINGS_CHECK_INT(out, 10);
    CLINGS_CHECK_INT(parse_and_sum(NULL, 4, &out), -1);
    CLINGS_CHECK_INT(parse_and_sum(values, 4, NULL), -1);
    return clings_report();
}
