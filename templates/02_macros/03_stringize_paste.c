/*
 * clings exercise: 02_macros/03_stringize_paste
 * title: Stringizing and token pasting
 * objective: Use # to stringize and ## to paste tokens.
 * hint: A second helper macro is needed to expand a macro before stringizing it.
 */

#include "clings/test.h"

#define CLINGS_VALUE 123

#define STRINGIFY_IMPL(x) #x
/* TODO: expand x before stringizing it. */
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
