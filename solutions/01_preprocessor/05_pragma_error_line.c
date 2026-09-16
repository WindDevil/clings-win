/*
 * clings 练习: 01_preprocessor/05_pragma_error_line
 * title: #error、#line 与 #pragma pack
 * objective: 使用诊断、行控制和打包编译指示。
 * hint: #pragma pack(push, 1) 会去掉两个成员之间的填充。
 */

#include "clings/test.h"

#include <stddef.h>

#if 0
#error "this branch is disabled"
#endif

#pragma pack(push, 1)
struct packed {
    char first;
    int second;
};
#pragma pack(pop)

int packed_size(void)
{
    return (int)sizeof(struct packed);
}

int line_number(void)
{
#line 1000
    return __LINE__;
}

int main(void)
{
    CLINGS_CHECK_INT(packed_size(), (int)(sizeof(char) + sizeof(int)));
    CLINGS_CHECK_INT(line_number(), 1000);
    return clings_report();
}
