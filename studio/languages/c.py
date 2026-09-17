"""C, as the editor understands it.

The interesting decision here is that this module does not try to understand C
at all.  It asks the compiler the exercise is built with - the bundled gcc,
the same flags, the same headers - and turns the answer into structured
diagnostics.  A hand-written C parser could be friendlier about a half-typed
line, and it would also be wrong about the fifty things this language does
that surprise people, which for a teaching exercise is the worst possible
failure mode: the editor would say the code is fine and `run` would disagree.

Completion has no compiler to lean on, so it is assembled: the language's own
keywords, a table of the standard library below, and the symbols the exercise
and the bundled test header actually declare.  The last part is what makes it
useful here - `CLINGS_CHECK_INT` and the functions of the exercise being
edited are the names a learner is reaching for.
"""

from __future__ import annotations

import dataclasses
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from .. import paths
from .base import CheckContext, Completion, Diagnostic, Language

# One line of gcc diagnostics:  <file>:<line>:<col>: <severity>: <message>
# The file part is lazy on purpose - on Windows it starts with a drive letter
# and a colon, so a greedy "[^:]+" would stop at "D".
DIAGNOSTIC_RE = re.compile(
    r"^(?P<file>.+?):(?P<line>\d+):(?P<col>\d+): "
    r"(?P<severity>fatal error|error|warning|note|info): (?P<message>.*)$"
)
# "... [-Werror=format=]" or "... [-Wunused-variable]"
FLAG_RE = re.compile(r"\s*\[(?P<code>-W[^\]]+)\]\s*$")
# "D:\...\main.c: In function 'read_number':" - context for what follows.  The
# path in front of it is the temporary copy, so only the tail is kept.
LEADING_CONTEXT_RE = re.compile(r"^\S.*?:\s+(?P<what>In \w+ .*|At top level):$")
# "In file included from D:\...\config.h:5:" - also context, and the one place
# a path has to be translated rather than dropped.
INCLUDED_FROM_RE = re.compile(
    r"^In file included from (?P<file>.+?):(?P<line>\d+)(?:,\s*from .*)?:$"
)
# How many echo lines (the source line plus its carets) to keep per diagnostic.
CONTEXT_LINES = 4
CHECK_TIMEOUT = 60.0

# The standard library the exercises actually use, as `header|name|signature`.
# Kept as a table because the interesting part is the data, not the parser:
# adding a function should be one line, and reviewing it should be reading one
# line.  Signatures are the declaration, so the editor can show them as-is.
STDLIB_TABLE = """
# --- <stdio.h> -------------------------------------------------------------
stdio.h|FILE|typedef struct _IO_FILE FILE;
stdio.h|stdin|FILE *stdin;
stdio.h|stdout|FILE *stdout;
stdio.h|stderr|FILE *stderr;
stdio.h|EOF|#define EOF (-1)
stdio.h|BUFSIZ|#define BUFSIZ 512
stdio.h|SEEK_SET|#define SEEK_SET 0
stdio.h|SEEK_CUR|#define SEEK_CUR 1
stdio.h|SEEK_END|#define SEEK_END 2
stdio.h|printf|int printf(const char *format, ...);
stdio.h|fprintf|int fprintf(FILE *stream, const char *format, ...);
stdio.h|sprintf|int sprintf(char *str, const char *format, ...);
stdio.h|snprintf|int snprintf(char *str, size_t size, const char *format, ...);
stdio.h|vprintf|int vprintf(const char *format, va_list ap);
stdio.h|vfprintf|int vfprintf(FILE *stream, const char *format, va_list ap);
stdio.h|vsnprintf|int vsnprintf(char *str, size_t size, const char *format, va_list ap);
stdio.h|scanf|int scanf(const char *format, ...);
stdio.h|fscanf|int fscanf(FILE *stream, const char *format, ...);
stdio.h|sscanf|int sscanf(const char *str, const char *format, ...);
stdio.h|fgets|char *fgets(char *s, int size, FILE *stream);
stdio.h|fputs|int fputs(const char *s, FILE *stream);
stdio.h|puts|int puts(const char *s);
stdio.h|fgetc|int fgetc(FILE *stream);
stdio.h|getc|int getc(FILE *stream);
stdio.h|getchar|int getchar(void);
stdio.h|fputc|int fputc(int c, FILE *stream);
stdio.h|putc|int putc(int c, FILE *stream);
stdio.h|putchar|int putchar(int c);
stdio.h|ungetc|int ungetc(int c, FILE *stream);
stdio.h|fopen|FILE *fopen(const char *path, const char *mode);
stdio.h|freopen|FILE *freopen(const char *path, const char *mode, FILE *stream);
stdio.h|fclose|int fclose(FILE *stream);
stdio.h|fflush|int fflush(FILE *stream);
stdio.h|fread|size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream);
stdio.h|fwrite|size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream);
stdio.h|fseek|int fseek(FILE *stream, long offset, int whence);
stdio.h|ftell|long ftell(FILE *stream);
stdio.h|rewind|void rewind(FILE *stream);
stdio.h|fgetpos|int fgetpos(FILE *stream, fpos_t *pos);
stdio.h|fsetpos|int fsetpos(FILE *stream, const fpos_t *pos);
stdio.h|feof|int feof(FILE *stream);
stdio.h|ferror|int ferror(FILE *stream);
stdio.h|clearerr|void clearerr(FILE *stream);
stdio.h|perror|void perror(const char *s);
stdio.h|remove|int remove(const char *path);
stdio.h|rename|int rename(const char *old_path, const char *new_path);
stdio.h|tmpfile|FILE *tmpfile(void);
stdio.h|setvbuf|int setvbuf(FILE *stream, char *buf, int mode, size_t size);
stdio.h|setbuf|void setbuf(FILE *stream, char *buf);
stdio.h|fileno|int fileno(FILE *stream);
stdio.h|fdopen|FILE *fdopen(int fd, const char *mode);
stdio.h|getline|ssize_t getline(char **lineptr, size_t *n, FILE *stream);
stdio.h|popen|FILE *popen(const char *command, const char *type);
stdio.h|pclose|int pclose(FILE *stream);
# --- <stdlib.h> ------------------------------------------------------------
stdlib.h|EXIT_SUCCESS|#define EXIT_SUCCESS 0
stdlib.h|EXIT_FAILURE|#define EXIT_FAILURE 1
stdlib.h|RAND_MAX|#define RAND_MAX 32767
stdlib.h|MB_CUR_MAX|size_t MB_CUR_MAX;
stdlib.h|malloc|void *malloc(size_t size);
stdlib.h|calloc|void *calloc(size_t nmemb, size_t size);
stdlib.h|realloc|void *realloc(void *ptr, size_t size);
stdlib.h|free|void free(void *ptr);
stdlib.h|atoi|int atoi(const char *nptr);
stdlib.h|atol|long atol(const char *nptr);
stdlib.h|atoll|long long atoll(const char *nptr);
stdlib.h|atof|double atof(const char *nptr);
stdlib.h|strtol|long strtol(const char *nptr, char **endptr, int base);
stdlib.h|strtoul|unsigned long strtoul(const char *nptr, char **endptr, int base);
stdlib.h|strtoll|long long strtoll(const char *nptr, char **endptr, int base);
stdlib.h|strtoull|unsigned long long strtoull(const char *nptr, char **endptr, int base);
stdlib.h|strtod|double strtod(const char *nptr, char **endptr);
stdlib.h|strtof|float strtof(const char *nptr, char **endptr);
stdlib.h|strtold|long double strtold(const char *nptr, char **endptr);
stdlib.h|rand|int rand(void);
stdlib.h|srand|void srand(unsigned int seed);
stdlib.h|qsort|void qsort(void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *));
stdlib.h|bsearch|void *bsearch(const void *key, const void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *));
stdlib.h|abs|int abs(int j);
stdlib.h|labs|long labs(long j);
stdlib.h|llabs|long long llabs(long long j);
stdlib.h|div|div_t div(int numerator, int denominator);
stdlib.h|ldiv|ldiv_t ldiv(long numerator, long denominator);
stdlib.h|lldiv|lldiv_t lldiv(long long numerator, long long denominator);
stdlib.h|exit|void exit(int status);
stdlib.h|atexit|int atexit(void (*function)(void));
stdlib.h|abort|void abort(void);
stdlib.h|getenv|char *getenv(const char *name);
stdlib.h|system|int system(const char *command);
stdlib.h|div_t|typedef struct { int quot; int rem; } div_t;
stdlib.h|ldiv_t|typedef struct { long quot; long rem; } ldiv_t;
# --- <string.h> ------------------------------------------------------------
string.h|strlen|size_t strlen(const char *s);
string.h|strcpy|char *strcpy(char *dest, const char *src);
string.h|strncpy|char *strncpy(char *dest, const char *src, size_t n);
string.h|strcat|char *strcat(char *dest, const char *src);
string.h|strncat|char *strncat(char *dest, const char *src, size_t n);
string.h|strcmp|int strcmp(const char *s1, const char *s2);
string.h|strncmp|int strncmp(const char *s1, const char *s2, size_t n);
string.h|strchr|char *strchr(const char *s, int c);
string.h|strrchr|char *strrchr(const char *s, int c);
string.h|strstr|char *strstr(const char *haystack, const char *needle);
string.h|strtok|char *strtok(char *str, const char *delim);
string.h|strspn|size_t strspn(const char *s, const char *accept);
string.h|strcspn|size_t strcspn(const char *s, const char *reject);
string.h|strpbrk|char *strpbrk(const char *s, const char *accept);
string.h|strdup|char *strdup(const char *s);
string.h|strerror|char *strerror(int errnum);
string.h|strcoll|int strcoll(const char *s1, const char *s2);
string.h|strxfrm|size_t strxfrm(char *dest, const char *src, size_t n);
string.h|memset|void *memset(void *s, int c, size_t n);
string.h|memcpy|void *memcpy(void *dest, const void *src, size_t n);
string.h|memmove|void *memmove(void *dest, const void *src, size_t n);
string.h|memcmp|int memcmp(const void *s1, const void *s2, size_t n);
string.h|memchr|void *memchr(const void *s, int c, size_t n);
# --- <math.h> --------------------------------------------------------------
math.h|M_PI|#define M_PI 3.14159265358979323846
math.h|INFINITY|#define INFINITY (__builtin_inff())
math.h|NAN|#define NAN (__builtin_nanf(""))
math.h|fabs|double fabs(double x);
math.h|fabsf|float fabsf(float x);
math.h|fmod|double fmod(double x, double y);
math.h|pow|double pow(double x, double y);
math.h|sqrt|double sqrt(double x);
math.h|cbrt|double cbrt(double x);
math.h|hypot|double hypot(double x, double y);
math.h|exp|double exp(double x);
math.h|exp2|double exp2(double x);
math.h|log|double log(double x);
math.h|log2|double log2(double x);
math.h|log10|double log10(double x);
math.h|sin|double sin(double x);
math.h|cos|double cos(double x);
math.h|tan|double tan(double x);
math.h|asin|double asin(double x);
math.h|acos|double acos(double x);
math.h|atan|double atan(double x);
math.h|atan2|double atan2(double y, double x);
math.h|sinh|double sinh(double x);
math.h|cosh|double cosh(double x);
math.h|tanh|double tanh(double x);
math.h|ceil|double ceil(double x);
math.h|floor|double floor(double x);
math.h|round|double round(double x);
math.h|trunc|double trunc(double x);
math.h|fmin|double fmin(double x, double y);
math.h|fmax|double fmax(double x, double y);
math.h|fdim|double fdim(double x, double y);
math.h|copysign|double copysign(double x, double y);
math.h|frexp|double frexp(double value, int *exp);
math.h|ldexp|double ldexp(double x, int exp);
math.h|modf|double modf(double value, double *iptr);
math.h|nan|double nan(const char *tagp);
math.h|isnan|int isnan(double x);
math.h|isinf|int isinf(double x);
math.h|isfinite|int isfinite(double x);
math.h|isnormal|int isnormal(double x);
# --- <ctype.h> -------------------------------------------------------------
ctype.h|isalpha|int isalpha(int c);
ctype.h|isdigit|int isdigit(int c);
ctype.h|isalnum|int isalnum(int c);
ctype.h|isspace|int isspace(int c);
ctype.h|isupper|int isupper(int c);
ctype.h|islower|int islower(int c);
ctype.h|ispunct|int ispunct(int c);
ctype.h|isprint|int isprint(int c);
ctype.h|isgraph|int isgraph(int c);
ctype.h|iscntrl|int iscntrl(int c);
ctype.h|isxdigit|int isxdigit(int c);
ctype.h|isblank|int isblank(int c);
ctype.h|toupper|int toupper(int c);
ctype.h|tolower|int tolower(int c);
# --- <assert.h> ------------------------------------------------------------
assert.h|assert|void assert(int expression);
assert.h|static_assert|_Static_assert(expression, message);
assert.h|NDEBUG|#define NDEBUG
# --- <stdbool.h> -----------------------------------------------------------
stdbool.h|bool|#define bool _Bool
stdbool.h|true|#define true 1
stdbool.h|false|#define false 0
# --- <stdint.h> ------------------------------------------------------------
stdint.h|int8_t|typedef signed char int8_t;
stdint.h|int16_t|typedef short int16_t;
stdint.h|int32_t|typedef int int32_t;
stdint.h|int64_t|typedef long long int64_t;
stdint.h|uint8_t|typedef unsigned char uint8_t;
stdint.h|uint16_t|typedef unsigned short uint16_t;
stdint.h|uint32_t|typedef unsigned int uint32_t;
stdint.h|uint64_t|typedef unsigned long long uint64_t;
stdint.h|intptr_t|typedef long long intptr_t;
stdint.h|uintptr_t|typedef unsigned long long uintptr_t;
stdint.h|intmax_t|typedef long long intmax_t;
stdint.h|uintmax_t|typedef unsigned long long uintmax_t;
stdint.h|INT8_MIN|#define INT8_MIN (-128)
stdint.h|INT8_MAX|#define INT8_MAX 127
stdint.h|UINT8_MAX|#define UINT8_MAX 255
stdint.h|INT16_MAX|#define INT16_MAX 32767
stdint.h|UINT16_MAX|#define UINT16_MAX 65535
stdint.h|INT32_MAX|#define INT32_MAX 2147483647
stdint.h|UINT32_MAX|#define UINT32_MAX 4294967295U
stdint.h|INT64_MAX|#define INT64_MAX 9223372036854775807LL
stdint.h|UINT64_MAX|#define UINT64_MAX 18446744073709551615ULL
stdint.h|SIZE_MAX|#define SIZE_MAX 18446744073709551615ULL
# --- <stddef.h> ------------------------------------------------------------
stddef.h|size_t|typedef unsigned long long size_t;
stddef.h|ptrdiff_t|typedef long long ptrdiff_t;
stddef.h|wchar_t|typedef unsigned short wchar_t;
stddef.h|NULL|#define NULL ((void *)0)
stddef.h|offsetof|size_t offsetof(type, member);
stddef.h|max_align_t|typedef struct { long long a; long double b; } max_align_t;
# --- <limits.h> and <float.h> ---------------------------------------------
limits.h|CHAR_BIT|#define CHAR_BIT 8
limits.h|CHAR_MIN|#define CHAR_MIN (-128)
limits.h|CHAR_MAX|#define CHAR_MAX 127
limits.h|SCHAR_MIN|#define SCHAR_MIN (-128)
limits.h|SCHAR_MAX|#define SCHAR_MAX 127
limits.h|UCHAR_MAX|#define UCHAR_MAX 255
limits.h|SHRT_MIN|#define SHRT_MIN (-32768)
limits.h|SHRT_MAX|#define SHRT_MAX 32767
limits.h|USHRT_MAX|#define USHRT_MAX 65535
limits.h|INT_MIN|#define INT_MIN (-2147483647 - 1)
limits.h|INT_MAX|#define INT_MAX 2147483647
limits.h|UINT_MAX|#define UINT_MAX 4294967295U
limits.h|LONG_MIN|#define LONG_MIN (-2147483647L - 1)
limits.h|LONG_MAX|#define LONG_MAX 2147483647L
limits.h|ULONG_MAX|#define ULONG_MAX 4294967295UL
limits.h|LLONG_MIN|#define LLONG_MIN (-9223372036854775807LL - 1)
limits.h|LLONG_MAX|#define LLONG_MAX 9223372036854775807LL
limits.h|ULLONG_MAX|#define ULLONG_MAX 18446744073709551615ULL
float.h|FLT_MAX|#define FLT_MAX 3.40282347e+38F
float.h|FLT_MIN|#define FLT_MIN 1.17549435e-38F
float.h|FLT_EPSILON|#define FLT_EPSILON 1.19209290e-7F
float.h|FLT_DIG|#define FLT_DIG 6
float.h|DBL_MAX|#define DBL_MAX 1.7976931348623157e+308
float.h|DBL_MIN|#define DBL_MIN 2.2250738585072014e-308
float.h|DBL_EPSILON|#define DBL_EPSILON 2.2204460492503131e-16
float.h|DBL_DIG|#define DBL_DIG 15
# --- <time.h> --------------------------------------------------------------
time.h|time_t|typedef long long time_t;
time.h|clock_t|typedef long clock_t;
time.h|struct tm|struct tm { int tm_sec, tm_min, tm_hour, tm_mday, tm_mon, tm_year, tm_wday, tm_yday, tm_isdst; };
time.h|CLOCKS_PER_SEC|#define CLOCKS_PER_SEC 1000
time.h|time|time_t time(time_t *tloc);
time.h|clock|clock_t clock(void);
time.h|difftime|double difftime(time_t time1, time_t time0);
time.h|mktime|time_t mktime(struct tm *timeptr);
time.h|localtime|struct tm *localtime(const time_t *timer);
time.h|gmtime|struct tm *gmtime(const time_t *timer);
time.h|asctime|char *asctime(const struct tm *timeptr);
time.h|ctime|char *ctime(const time_t *timer);
time.h|strftime|size_t strftime(char *s, size_t max, const char *format, const struct tm *tm);
# --- <errno.h> -------------------------------------------------------------
errno.h|errno|int errno;
errno.h|EDOM|#define EDOM 33
errno.h|ERANGE|#define ERANGE 34
errno.h|EILSEQ|#define EILSEQ 42
# --- <stdarg.h> ------------------------------------------------------------
stdarg.h|va_list|typedef __builtin_va_list va_list;
stdarg.h|va_start|void va_start(va_list ap, last);
stdarg.h|va_arg|type va_arg(va_list ap, type);
stdarg.h|va_end|void va_end(va_list ap);
stdarg.h|va_copy|void va_copy(va_list dest, va_list src);
# --- <signal.h> ------------------------------------------------------------
signal.h|signal|void (*signal(int sig, void (*func)(int)))(int);
signal.h|raise|int raise(int sig);
signal.h|SIGINT|#define SIGINT 2
signal.h|SIGSEGV|#define SIGSEGV 11
signal.h|SIGABRT|#define SIGABRT 22
signal.h|SIG_DFL|#define SIG_DFL ((void (*)(int))0)
signal.h|SIG_IGN|#define SIG_IGN ((void (*)(int))1)
# --- <setjmp.h> ------------------------------------------------------------
setjmp.h|jmp_buf|typedef struct __jmp_buf_tag jmp_buf[1];
setjmp.h|setjmp|int setjmp(jmp_buf env);
setjmp.h|longjmp|void longjmp(jmp_buf env, int val);
# --- <locale.h> ------------------------------------------------------------
locale.h|setlocale|char *setlocale(int category, const char *locale);
locale.h|localeconv|struct lconv *localeconv(void);
locale.h|LC_ALL|#define LC_ALL 6
# --- <stdatomic.h> ---------------------------------------------------------
stdatomic.h|atomic_int|typedef _Atomic int atomic_int;
stdatomic.h|atomic_bool|typedef _Atomic _Bool atomic_bool;
stdatomic.h|atomic_flag|typedef struct { _Bool value; } atomic_flag;
stdatomic.h|atomic_init|void atomic_init(volatile A *obj, C value);
stdatomic.h|atomic_load|C atomic_load(const volatile A *obj);
stdatomic.h|atomic_store|void atomic_store(volatile A *obj, C desired);
stdatomic.h|atomic_fetch_add|C atomic_fetch_add(volatile A *obj, M operand);
stdatomic.h|atomic_compare_exchange_strong|_Bool atomic_compare_exchange_strong(volatile A *obj, C *expected, C desired);
stdatomic.h|atomic_flag_test_and_set|_Bool atomic_flag_test_and_set(volatile atomic_flag *obj);
stdatomic.h|atomic_flag_clear|void atomic_flag_clear(volatile atomic_flag *obj);
stdatomic.h|memory_order_seq_cst|memory_order_seq_cst;
stdatomic.h|memory_order_acquire|memory_order_acquire;
stdatomic.h|memory_order_release|memory_order_release;
stdatomic.h|memory_order_relaxed|memory_order_relaxed;
stdatomic.h|ATOMIC_VAR_INIT|#define ATOMIC_VAR_INIT(value) (value)
# --- <threads.h> and <pthread.h> ------------------------------------------
threads.h|thrd_t|typedef struct { void *handle; } thrd_t;
threads.h|mtx_t|typedef struct { void *handle; } mtx_t;
threads.h|thrd_create|int thrd_create(thrd_t *thr, int (*func)(void *), void *arg);
threads.h|thrd_join|int thrd_join(thrd_t thr, int *res);
threads.h|mtx_lock|int mtx_lock(mtx_t *mtx);
threads.h|mtx_unlock|int mtx_unlock(mtx_t *mtx);
pthread.h|pthread_t|typedef unsigned long pthread_t;
pthread.h|pthread_mutex_t|typedef struct { void *handle; } pthread_mutex_t;
pthread.h|pthread_create|int pthread_create(pthread_t *thread, const pthread_attr_t *attr, void *(*start)(void *), void *arg);
pthread.h|pthread_join|int pthread_join(pthread_t thread, void **retval);
pthread.h|pthread_exit|void pthread_exit(void *retval);
pthread.h|pthread_self|pthread_t pthread_self(void);
pthread.h|pthread_mutex_init|int pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr);
pthread.h|pthread_mutex_lock|int pthread_mutex_lock(pthread_mutex_t *mutex);
pthread.h|pthread_mutex_unlock|int pthread_mutex_unlock(pthread_mutex_t *mutex);
pthread.h|pthread_mutex_destroy|int pthread_mutex_destroy(pthread_mutex_t *mutex);
pthread.h|pthread_mutex_trylock|int pthread_mutex_trylock(pthread_mutex_t *mutex);
pthread.h|pthread_cond_init|int pthread_cond_init(pthread_cond_t *cond, const pthread_condattr_t *attr);
pthread.h|pthread_cond_wait|int pthread_cond_wait(pthread_cond_t *cond, pthread_mutex_t *mutex);
pthread.h|pthread_cond_signal|int pthread_cond_signal(pthread_cond_t *cond);
pthread.h|pthread_cond_broadcast|int pthread_cond_broadcast(pthread_cond_t *cond);
# --- <unistd.h> (POSIX, -D_POSIX_C_SOURCE=200809L) -------------------------
unistd.h|read|ssize_t read(int fd, void *buf, size_t count);
unistd.h|write|ssize_t write(int fd, const void *buf, size_t count);
unistd.h|close|int close(int fd);
unistd.h|sleep|unsigned int sleep(unsigned int seconds);
unistd.h|usleep|int usleep(useconds_t usec);
unistd.h|getpid|pid_t getpid(void);
unistd.h|access|int access(const char *path, int mode);
unistd.h|unlink|int unlink(const char *path);
unistd.h|STDIN_FILENO|#define STDIN_FILENO 0
unistd.h|STDOUT_FILENO|#define STDOUT_FILENO 1
unistd.h|STDERR_FILENO|#define STDERR_FILENO 2
"""

KEYWORDS = (
    "auto break case char const continue default do double else enum extern "
    "float for goto if inline int long register restrict return short signed "
    "sizeof static struct switch typedef union unsigned void volatile while"
).split()
C11_KEYWORDS = (
    "_Alignas _Alignof _Atomic _Bool _Complex _Generic _Imaginary _Noreturn "
    "_Static_assert _Thread_local"
).split()
TYPES = (
    "size_t ssize_t ptrdiff_t wchar_t bool true false NULL FILE fpos_t "
    "va_list jmp_buf div_t ldiv_t lldiv_t sig_atomic_t clock_t time_t "
    "atomic_int atomic_flag atomic_bool memory_order"
).split()

SNIPPETS: tuple[tuple[str, str, str], ...] = (
    ("main", "int main(void)\n{\n    \n    return 0;\n}\n", "程序入口"),
    ("for", "for (int i = 0; i < n; i++) {\n    \n}\n", "计数循环"),
    ("while", "while (condition) {\n    \n}\n", "while 循环"),
    ("if", "if (condition) {\n    \n}\n", "条件分支"),
    ("ifelse", "if (condition) {\n    \n} else {\n    \n}\n", "if / else"),
    ("switch", "switch (value) {\ncase 1:\n    break;\ndefault:\n    break;\n}\n", "switch 分支"),
    ("printf", 'printf("%d\\n", value);\n', "打印整数"),
    ("printf_str", 'printf("%s\\n", text);\n', "打印字符串"),
    ("scanf", 'if (scanf("%d", &value) != 1) {\n    return 1;\n}\n', "读入整数并检查返回值"),
    ("malloc", "int *data = malloc(count * sizeof *data);\nif (data == NULL) {\n    return 1;\n}\n", "分配并检查 NULL"),
    ("struct", "struct name {\n    int field;\n};\n", "结构体定义"),
    ("include_test", '#include "clings/test.h"\n', "每个练习都必须包含"),
)


def _table() -> tuple[Completion, ...]:
    """Parse STDLIB_TABLE once, at import."""
    items: list[Completion] = []
    for raw in STDLIB_TABLE.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "|" not in line:
            continue
        header, name, signature = (part.strip() for part in line.split("|", 2))
        if signature.startswith(("#define", "typedef")):
            kind = "macro" if signature.startswith("#define") else "type"
        elif signature.startswith("struct "):
            kind = "type"
        else:
            kind = "function"
        items.append(
            Completion(
                label=name,
                kind=kind,
                detail=signature,
                insert=name,
                header=f"<{header}>",
            )
        )
    return tuple(items)


STDLIB = _table()
STDLIB_BY_NAME = {item.label: item for item in STDLIB}

# Functions and macros the exercise (or the bundled test header) declares.
DECL_RE = re.compile(
    r"^[ \t]*(?!return\b)(?:static\s+|inline\s+|extern\s+|const\s+)*"
    r"[A-Za-z_][A-Za-z0-9_ \t]*[\s\*]+(?P<name>[A-Za-z_]\w*)\s*\(",
    re.MULTILINE,
)
DEFINE_RE = re.compile(r"^[ \t]*#\s*define\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE)
TYPEDEF_RE = re.compile(
    r"^[ \t]*typedef\b[^;]*?(?P<name>[A-Za-z_]\w*)\s*;", re.MULTILINE
)
STRUCT_RE = re.compile(r"^[ \t]*(?:struct|union|enum)\s+(?P<name>[A-Za-z_]\w*)", re.MULTILINE)


def _local_completions(root: Path, path: Path, content: str, context: CheckContext) -> list[Completion]:
    """Names declared by this exercise and by the bundled test framework.

    Read as text with regular expressions rather than parsed: the aim is for
    the editor to offer `print_greeting` once the learner has typed it, and a
    regex that finds most declarations is worth more here than a real parser
    that has to be right about all of them.
    """
    found: dict[str, Completion] = {}
    sources: list[tuple[Path, str]] = []
    test_header = root / "include" / "clings" / "test.h"
    if test_header.is_file():
        try:
            sources.append((test_header, test_header.read_text(encoding="utf-8")))
        except OSError:
            pass
    sources.append((path, content))
    for other in context.exercise_files:
        if other == path:
            continue
        try:
            sources.append((other, other.read_text(encoding="utf-8")))
        except OSError:
            continue

    for source_path, text in sources:
        if source_path == test_header:
            origin = "clings/test.h"
        else:
            origin = "本练习"
        for name in DEFINE_RE.findall(text):
            found.setdefault(
                name, Completion(label=name, kind="macro", detail="#define", header=origin)
            )
        for name in TYPEDEF_RE.findall(text):
            found.setdefault(
                name, Completion(label=name, kind="type", detail="typedef", header=origin)
            )
        for name in STRUCT_RE.findall(text):
            found.setdefault(
                name, Completion(label=name, kind="type", detail="struct", header=origin)
            )
        for name in DECL_RE.findall(text):
            if name in {"if", "for", "while", "switch", "sizeof", "return"}:
                continue
            found.setdefault(
                name,
                Completion(label=name, kind="function", detail="本文件里的函数", header=origin),
            )
    return list(found.values())


class CLanguage(Language):
    id = "c"
    label = "C"
    extensions = (".c", ".h")
    # CodeMirror's C mode; the "clike" mode also covers C++ and Java, which is
    # why the id is not simply "c".
    editor_mode = "text/x-csrc"
    line_comment = "//"
    block_comment = ("/*", "*/")
    tab_size = 4
    checks = True
    completes = True

    # -- diagnostics ------------------------------------------------------
    def check(self, path: Path, content: str, context: CheckContext) -> list[Diagnostic]:
        """Compile the exercise, with the editor's text in place of the file.

        The whole exercise is copied into a temporary directory rather than
        compiled where it lives: a header cannot be checked on its own, the
        learner's unsaved text has to be the thing compiled, and nothing the
        editor does should leave a file behind in exercises/.
        """
        compiler = context.toolchain.compiler
        if not context.toolchain.compiler_found:
            return [
                Diagnostic(
                    line=1,
                    column=1,
                    severity="info",
                    message=f"没有找到编译器 {compiler}，暂时无法检查语法。"
                    "先运行 .\\clings.cmd doctor 看看工具链。",
                )
            ]

        with tempfile.TemporaryDirectory(prefix="clings-check-") as work:
            staged = self._stage(Path(work), path, content, context)
            if not staged.sources:
                return []
            command = [
                compiler,
                *context.toolchain.cflags,
                "-fsyntax-only",
                f"-I{context.root / 'include'}",
                f"-I{staged.directory}",
                *[str(source) for source in staged.sources],
            ]
            try:
                result = subprocess.run(
                    command,
                    cwd=str(context.root),
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    timeout=CHECK_TIMEOUT,
                    check=False,
                )
            except (OSError, subprocess.TimeoutExpired) as error:
                return [
                    Diagnostic(
                        line=1,
                        column=1,
                        severity="info",
                        message=f"编译器没能运行: {error}",
                    )
                ]
        return self._parse(result.stdout, staged, path)

    @staticmethod
    def _stage(
        directory: Path, path: Path, content: str, context: CheckContext
    ) -> "_Staged":
        """Write the exercise's files into *directory*, editor text included."""
        staged = _Staged(directory=directory, originals={}, sources=[])
        for original in context.exercise_files or (path,):
            name = original.name
            if original.suffix.lower() not in {".c", ".h"}:
                continue
            target = directory / name
            if original == path:
                target.write_text(content, encoding="utf-8")
            else:
                try:
                    shutil.copyfile(original, target)
                except OSError:
                    continue
            staged.originals[target] = original
        staged.sources = sorted(
            (target for target in staged.originals if target.suffix == ".c"),
            key=lambda target: (target.name != path.name, target.name),
        )
        return staged

    @staticmethod
    def _parse(output: str, staged: "_Staged", path: Path) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        pending: list[str] = []
        # How the compiler got here.  Kept apart from the message because a
        # header is compiled once per translation unit that includes it, and
        # the chain is the only thing that differs between those reports: in
        # the message it would turn one mistake into one entry per .c file.
        chain: list[str] = []
        for line in output.splitlines():
            match = DIAGNOSTIC_RE.match(line)
            if not match:
                lead = LEADING_CONTEXT_RE.match(line)
                included = INCLUDED_FROM_RE.match(line)
                if lead:
                    pending.append(lead.group("what"))
                elif included:
                    # Only reachable for a diagnostic in a header, which is
                    # where "included from" chains point.
                    origin = staged.label(Path(included.group("file")))
                    chain.append(f"经由 {origin}:{included.group('line')} 引入")
                elif line[:1].isspace() and diagnostics:
                    # The source line, then the caret art gcc echoes back under
                    # it.  Keep a few lines: the carets are what make "expected
                    # 'int *'" legible.
                    previous = diagnostics[-1]
                    if previous.context.count("\n") < CONTEXT_LINES:
                        diagnostics[-1] = dataclasses.replace(
                            previous,
                            context="\n".join(
                                filter(None, (previous.context, line.rstrip()))
                            ),
                        )
                continue
            message = match.group("message")
            code = ""
            flag = FLAG_RE.search(message)
            if flag:
                code = flag.group("code")
                message = FLAG_RE.sub("", message)
            origin = Path(match.group("file"))
            diagnostics.append(
                Diagnostic(
                    line=int(match.group("line")),
                    column=int(match.group("col")),
                    severity=(
                        "error" if match.group("severity").endswith("error") else match.group("severity")
                    ),
                    message=f"{' '.join(pending)}{': ' if pending else ''}{message}",
                    file=staged.label(origin),
                    code=code,
                    context="\n".join(chain),
                )
            )
            pending = []
            chain = []

        # One mistake often earns the same note twice, once per use of the
        # macro that carried it; the editor's list should not say so twice.
        unique: dict[tuple, Diagnostic] = {}
        for item in diagnostics:
            key = (item.file, item.line, item.column, item.severity, item.message, item.code)
            unique.setdefault(key, item)
        # The edited file's own diagnostics come first: the editor is showing
        # that file, and a problem in a header it includes is second news.
        own = paths.relative(path)
        return sorted(
            unique.values(), key=lambda item: (item.file != own, item.line, item.column)
        )

    # -- completion -------------------------------------------------------
    def completions(
        self, path: Path, content: str, context: CheckContext
    ) -> list[Completion]:
        items: dict[str, Completion] = {}
        for keyword in (*KEYWORDS, *C11_KEYWORDS):
            items[keyword] = Completion(
                label=keyword, kind="keyword", detail="关键字", header="C17"
            )
        for name in TYPES:
            items.setdefault(
                name, Completion(label=name, kind="type", detail="类型", header="C17")
            )
        for item in STDLIB:
            items.setdefault(item.label, item)
        for name, body, detail in SNIPPETS:
            items.setdefault(
                name, Completion(label=name, kind="snippet", detail=detail, insert=body)
            )
        # Whatever the exercise and test.h declare wins over the table: if the
        # learner wrote their own `printf`, that is the one they mean.
        for item in _local_completions(context.root, path, content, context):
            items[item.label] = item
        return [items[key] for key in sorted(items)]


class _Staged:
    """The temporary copy of an exercise a check runs against."""

    __slots__ = ("directory", "originals", "sources")

    def __init__(
        self, directory: Path, originals: dict[Path, Path], sources: list[Path]
    ) -> None:
        self.directory = directory
        self.originals = originals
        self.sources = sources

    def label(self, reported: Path) -> str:
        """Turn a path from the compiler's output back into ours.

        The compiled file is a copy in a temporary directory, so gcc reports
        the copy.  Anything the copy came from is mapped back to the real
        file; anything else (a header out of include/) is taken as it is,
        relative to the package.
        """
        name = os.path.basename(str(reported))
        for target, original in self.originals.items():
            if target.name == name:
                return paths.relative(original)
        for candidate in (reported, Path(name)):
            text = paths.relative(candidate)
            if not text.startswith(".."):
                return text
        return name
