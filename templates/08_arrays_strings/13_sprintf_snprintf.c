/*
 * clings 练习: 08_arrays_strings/13_sprintf_snprintf
 * title: sprintf 与 snprintf
 * objective: 用 snprintf 格式化文本，并理解截断行为。
 * hint: snprintf 返回的是「如果空间够，本会写出的字符数」。
 */

#include "clings/test.h"

#include <stdio.h>

int format_record(char *buffer, size_t size, const char *name, int age)
{
    /* TODO: 按「名字 年龄」的顺序格式化。 */
    return snprintf(buffer, size, "%d:%s", age, name);
}

int main(void)
{
    char buffer[32];
    char small[6];

    CLINGS_CHECK_INT(format_record(buffer, sizeof buffer, "Ada", 36), 6);
    CLINGS_CHECK_STR(buffer, "Ada:36");
    CLINGS_CHECK_INT(format_record(small, sizeof small, "Ada", 36), 6);
    CLINGS_CHECK_STR(small, "Ada:3");
    return clings_report();
}
