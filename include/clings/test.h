#ifndef CLINGS_TEST_H
#define CLINGS_TEST_H

/*
 * Thin assertion interface for clings exercises.
 *
 * The implementation lives in test.c, so including this header does not
 * transitively provide stdio.h, stdlib.h, or string.h to exercise code.
 */

void clings_record(int passed, const char *expr, const char *file, int line);

void clings_record_msg(int passed, const char *expr, const char *message,
                       const char *file, int line);

void clings_record_int(long long actual, long long expected,
                       const char *actual_expr, const char *expected_expr,
                       const char *file, int line);

void clings_record_str(const char *actual, const char *expected,
                       const char *actual_expr, const char *expected_expr,
                       const char *file, int line);

void clings_record_mem(const void *actual, const void *expected,
                       unsigned long size, const char *actual_expr,
                       const char *expected_expr, const char *file, int line);

int clings_report(void);

#define CLINGS_CHECK(expr) \
    clings_record(!!((expr)), #expr, __FILE__, __LINE__)

#define CLINGS_CHECK_MSG(expr, message) \
    clings_record_msg(!!((expr)), #expr, (message), __FILE__, __LINE__)

#define CLINGS_CHECK_INT(actual, expected)                                  \
    clings_record_int((long long)(actual), (long long)(expected), #actual,  \
                      #expected, __FILE__, __LINE__)

#define CLINGS_CHECK_STR(actual, expected)                                    \
    clings_record_str((actual), (expected), #actual, #expected, __FILE__,     \
                      __LINE__)

#define CLINGS_CHECK_MEM(actual, expected, size)                              \
    clings_record_mem((actual), (expected), (unsigned long)(size), #actual,   \
                      #expected, __FILE__, __LINE__)

#endif /* CLINGS_TEST_H */
