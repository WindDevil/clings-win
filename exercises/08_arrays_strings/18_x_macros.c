/*
 * clings 练习: 08_arrays_strings/18_x_macros
 * title: X-macro
 * objective: 用同一份列表生成枚举和字符串表。
 * hint: 字符串表用 #name 生成，不是写死的字符串。
 */

#include "clings/test.h"

#define COLOR_LIST(X) X(RED) X(GREEN) X(BLUE)

enum color {
#define X(name) COLOR_##name,
    COLOR_LIST(X)
#undef X
};

static const char *const color_names[] = {
/* TODO: 把每个名字字符串化。 */
#define X(name) "unknown",
    COLOR_LIST(X)
#undef X
};

int main(void)
{
    CLINGS_CHECK_STR(color_names[COLOR_RED], "RED");
    CLINGS_CHECK_STR(color_names[COLOR_GREEN], "GREEN");
    CLINGS_CHECK_STR(color_names[COLOR_BLUE], "BLUE");
    return clings_report();
}
