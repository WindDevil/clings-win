#include "clings/test.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/* 足够容纳任何练习的期望输出；更长的捕获只比较到
 * 这个长度，并如实报告被截断，而不是悄悄裁掉。 */
#define CLINGS_CAPTURE_SIZE 4096

/* 一个捕获到的字节最多转义成四个字符（"\x1f"），再加上结尾的 NUL。 */
#define CLINGS_ESCAPED_SIZE (CLINGS_CAPTURE_SIZE * 4 + 1)

static int clings_failures = 0;
static int clings_checks = 0;

static int clings_saved_stdout = -1;
static FILE *clings_capture_file = NULL;
static int clings_capture_failed = 0;
static int clings_truncated = 0;
static char clings_capture_text[CLINGS_CAPTURE_SIZE];
static char clings_escaped_actual[CLINGS_ESCAPED_SIZE];
static char clings_escaped_expected[CLINGS_ESCAPED_SIZE];

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

/*
 * 把文本写成「缺了什么一眼能看出来」的样子：如果报告原样打印，
 * "42" 和 "42\n" 会变成两行看上去一样的东西，
 * 而这正是这些检查要消除的困惑。
 */
static void clings_escape(const char *text, char *out, size_t size)
{
    size_t used = 0;
    size_t index;

    for (index = 0; text[index] != '\0' && used + 5 < size; ++index) {
        unsigned char byte = (unsigned char)text[index];

        switch (byte) {
        case '\n':
            out[used++] = '\\';
            out[used++] = 'n';
            break;
        case '\t':
            out[used++] = '\\';
            out[used++] = 't';
            break;
        case '\r':
            out[used++] = '\\';
            out[used++] = 'r';
            break;
        case '\\':
            out[used++] = '\\';
            out[used++] = '\\';
            break;
        case '"':
            out[used++] = '\\';
            out[used++] = '"';
            break;
        default:
            if (byte < 0x20 || byte == 0x7f) {
                used += (size_t)snprintf(out + used, size - used, "\\x%02x",
                                         byte);
            } else {
                out[used++] = (char)byte;
            }
            break;
        }
    }

    out[used] = '\0';
}

void clings_capture_begin(void)
{
    clings_capture_failed = 0;
    clings_truncated = 0;
    clings_capture_text[0] = '\0';

    fflush(stdout);

    /* 按描述符改写、而不是重新打开一个终端，stdout 原来是什么
     * 就还是什么：测试从管道、文件还是终端启动，
     * 输出就会回到它原来该去的地方。 */
    clings_saved_stdout = dup(fileno(stdout));
    clings_capture_file = tmpfile();
    if (clings_saved_stdout < 0 || clings_capture_file == NULL) {
        /* 两半里只要有一半失败，stdout 就还停在原地，
         * 就把成功的那一半撤掉，让检查如实报告失败。 */
        clings_capture_failed = 1;
        if (clings_saved_stdout >= 0) {
            close(clings_saved_stdout);
            clings_saved_stdout = -1;
        }
        if (clings_capture_file != NULL) {
            fclose(clings_capture_file);
            clings_capture_file = NULL;
        }
        return;
    }

    dup2(fileno(clings_capture_file), fileno(stdout));
}

void clings_capture_end(void)
{
    size_t got;

    if (clings_capture_file == NULL) {
        return;
    }

    fflush(stdout);
    dup2(clings_saved_stdout, fileno(stdout));
    close(clings_saved_stdout);
    clings_saved_stdout = -1;

    fseek(clings_capture_file, 0L, SEEK_SET);
    got = fread(clings_capture_text, 1, sizeof(clings_capture_text) - 1,
                clings_capture_file);
    clings_capture_text[got] = '\0';
    if (got == sizeof(clings_capture_text) - 1 &&
        fgetc(clings_capture_file) != EOF) {
        clings_truncated = 1;
    }

    fclose(clings_capture_file);
    clings_capture_file = NULL;
}

const char *clings_captured(void)
{
    return clings_capture_text;
}

void clings_record_stdout(const char *actual, const char *expected,
                          const char *actual_expr, const char *file, int line)
{
    ++clings_checks;

    clings_escape(actual ? actual : "", clings_escaped_actual,
                  sizeof(clings_escaped_actual));
    clings_escape(expected ? expected : "", clings_escaped_expected,
                  sizeof(clings_escaped_expected));

    if (clings_capture_failed) {
        ++clings_failures;
        fprintf(stderr, "  FAIL %s:%d: %s (stdout could not be captured)\n",
                file, line, actual_expr);
        return;
    }

    if (!clings_truncated && actual != NULL && expected != NULL &&
        strcmp(actual, expected) == 0) {
        printf("  ok   %s writes \"%s\"\n", actual_expr,
               clings_escaped_expected);
        return;
    }

    ++clings_failures;
    fprintf(stderr, "  FAIL %s:%d: %s writes \"%s\" (want \"%s\")%s\n", file,
            line, actual_expr, clings_escaped_actual, clings_escaped_expected,
            clings_truncated ? " (output truncated)" : "");
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
