#include "clings/test.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int clings_failures = 0;
static int clings_checks = 0;

void clings_record(int passed, const char *expr, const char *file, int line)
{
    ++clings_checks;
    if (passed) {
        printf("  ok   %s\n", expr);
        return;
    }

    ++clings_failures;
    fprintf(stderr, "  FAIL %s:%d: %s\n", file, line, expr);
}

void clings_record_msg(int passed, const char *expr, const char *message,
                       const char *file, int line)
{
    ++clings_checks;
    if (passed) {
        printf("  ok   %s\n", expr);
        return;
    }

    ++clings_failures;
    fprintf(stderr, "  FAIL %s:%d: %s (%s)\n", file, line, expr, message);
}

void clings_record_int(long long actual, long long expected,
                       const char *actual_expr, const char *expected_expr,
                       const char *file, int line)
{
    ++clings_checks;
    if (actual == expected) {
        printf("  ok   %s == %s\n", actual_expr, expected_expr);
        return;
    }

    ++clings_failures;
    fprintf(stderr, "  FAIL %s:%d: %s == %s (got %lld, want %lld)\n", file,
            line, actual_expr, expected_expr, actual, expected);
}

void clings_record_str(const char *actual, const char *expected,
                       const char *actual_expr, const char *expected_expr,
                       const char *file, int line)
{
    ++clings_checks;
    if (actual != NULL && expected != NULL && strcmp(actual, expected) == 0) {
        printf("  ok   %s == %s\n", actual_expr, expected_expr);
        return;
    }

    ++clings_failures;
    fprintf(stderr, "  FAIL %s:%d: %s == %s (got \"%s\", want \"%s\")\n", file,
            line, actual_expr, expected_expr, actual ? actual : "(null)",
            expected ? expected : "(null)");
}

void clings_record_mem(const void *actual, const void *expected,
                       unsigned long size, const char *actual_expr,
                       const char *expected_expr, const char *file, int line)
{
    ++clings_checks;
    if (memcmp(actual, expected, size) == 0) {
        printf("  ok   %s memory == %s\n", actual_expr, expected_expr);
        return;
    }

    ++clings_failures;
    fprintf(stderr, "  FAIL %s:%d: memory differs: %s vs %s\n", file, line,
            actual_expr, expected_expr);
}

int clings_report(void)
{
    if (clings_failures == 0) {
        printf("\nAll %d checks passed.\n", clings_checks);
        return EXIT_SUCCESS;
    }

    fprintf(stderr, "\n%d of %d checks failed.\n", clings_failures,
            clings_checks);
    return EXIT_FAILURE;
}
