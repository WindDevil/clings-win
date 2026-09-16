/*
 * clings 练习: 02_macros/01_object_macro
 * title: 对象式宏
 * objective: 使用一个有名字的编译期常量。
 * hint: 对象式宏就是简单的文本替换。
 */

#include "clings/test.h"

/* TODO: 定义一个 16 字节的缓冲区长度。 */
#define CLINGS_BUFFER_SIZE 8
#define CLINGS_VERSION 2

int buffer_size(void)
{
    return CLINGS_BUFFER_SIZE;
}

int version(void)
{
    return CLINGS_VERSION;
}

int main(void)
{
    CLINGS_CHECK_INT(buffer_size(), 16);
    CLINGS_CHECK_INT(version(), 2);
    return clings_report();
}
