#ifndef CLINGS_TEST_H
#define CLINGS_TEST_H

/*
 * clings 练习用的轻量断言接口。
 *
 * 实现放在 test.c 里，所以包含这个头文件并不会
 * 顺带把 stdio.h、stdlib.h、string.h 带进练习代码。
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

void clings_record_stdout(const char *actual, const char *expected,
                          const char *actual_expr, const char *file, int line);

/*
 * 要比较打印出来的文本，就得先拿到文本本身；而一个返回 printf 结果的
 * 函数交给测试的只是一个字符数。下面三个函数把进程的 stdout 临时改写
 * 到临时文件，检查结束后按描述符还原回去，再把写进去的内容抄进一个
 * 内部缓冲区。
 */
void clings_capture_begin(void);

void clings_capture_end(void);

const char *clings_captured(void);

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

/*
 * 运行 `call`，把它打印出来的全部内容与 `expected` 比较。`call` 的
 * 返回值不检查：文本对了，字符数自然是对的；文本错了，字符数本来
 * 也不是重点。
 */
#define CLINGS_CHECK_STDOUT(call, expected)                                   \
    do {                                                                      \
        clings_capture_begin();                                               \
        (void)(call);                                                         \
        clings_capture_end();                                                 \
        clings_record_stdout(clings_captured(), (expected), #call, __FILE__,  \
                             __LINE__);                                       \
    } while (0)

#endif /* CLINGS_TEST_H */
