/*
 * clings 练习: 00_basics/05_snprintf
 * title: 用 snprintf 安全格式化
 * objective: 把格式化文本写进固定大小的缓冲区。
 * hint: snprintf 接收缓冲区大小，返回它本会写出的字符数。
 */

#include "clings/test.h"

#include <stdio.h>

char buffer[32];

int format_greeting(void)
{
    return snprintf(buffer, 32, "Hello, %s", "C");
}

int main(void)
{
    CLINGS_CHECK_INT(format_greeting(), 8);
    CLINGS_CHECK_STR(buffer, "Hello, C");
    return clings_report();
}
