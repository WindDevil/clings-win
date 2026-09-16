/*
 * clings 练习: 02_macros/03_stringize_paste
 * title: 字符串化与记号拼接
 * objective: 用 # 做字符串化，用 ## 拼接记号。
 * hint: 要先把宏展开再字符串化，就得再套一层辅助宏。
 */

#include "clings/test.h"

#define CLINGS_VALUE 123

#define STRINGIFY_IMPL(x) #x
/* TODO: 先把 x 展开，再字符串化。 */
#define STRINGIFY(x) #x

#define CONCAT_IMPL(a, b) a##b
#define CONCAT(a, b) CONCAT_IMPL(a, b)

const char *stringized_value(void)
{
    return STRINGIFY(CLINGS_VALUE);
}

int concatenated_value(void)
{
    int CONCAT(foo, bar) = 42;
    return foobar;
}

int main(void)
{
    CLINGS_CHECK_STR(stringized_value(), "123");
    CLINGS_CHECK_INT(concatenated_value(), 42);
    return clings_report();
}
