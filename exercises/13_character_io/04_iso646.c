/*
 * clings 练习: 13_character_io/04_iso646
 * title: iso646.h 的替代写法
 * objective: 使用 iso646.h 里的 and/or/not。
 * hint: iso646.h 把 and 定义为 &&，把 or 定义为 ||。
 */

#include "clings/test.h"

#include <iso646.h>

int is_yes(const char *text)
{
    return /* TODO: accept either y or Y. */
    (text[0] == 'y' and text[0] == 'Y') and text[1] == '\0';
}

int main(void)
{
    CLINGS_CHECK_INT(is_yes("y"), 1);
    CLINGS_CHECK_INT(is_yes("Y"), 1);
    CLINGS_CHECK_INT(is_yes("yes"), 0);
    CLINGS_CHECK_INT(is_yes("n"), 0);
    return clings_report();
}
