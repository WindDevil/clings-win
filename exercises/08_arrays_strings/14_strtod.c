/*
 * clings 练习: 08_arrays_strings/14_strtod
 * title: 把字符串转成 double
 * objective: 用 strtod 解析 double，并拒绝多余的尾部输入。
 * hint: 要检查 errno、endptr，以及数字后面的那个字符。
 */

#include "clings/test.h"

#include <errno.h>
#include <stdlib.h>

int parse_double(const char *text, double *out)
{
    char *end = NULL;
    errno = 0;
    double value = strtod(text, &end);
    /* TODO: 拒绝多余的尾部字符。 */
    if (errno == ERANGE || end == text) {
        return -1;
    }
    *out = value;
    return 0;
}

int main(void)
{
    double value = 0.0;

    CLINGS_CHECK_INT(parse_double("3.14", &value), 0);
    CLINGS_CHECK_INT(value == 3.14, 1);
    CLINGS_CHECK_INT(parse_double("3.14x", &value), -1);
    CLINGS_CHECK_INT(parse_double("", &value), -1);
    return clings_report();
}
