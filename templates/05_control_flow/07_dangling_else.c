/*
 * clings 练习: 05_control_flow/07_dangling_else
 * title: 悬挂 else
 * objective: 用花括号让 else 绑定到预期的 if。
 * hint: 不写花括号时，else 会绑定到最近的那个还没配对的 if。
 */

#include "clings/test.h"

int classify(int x, int y)
{
    if (x > 0)
        if (y > 0)
            return 1;
    else
        return 2;
    return 0;
}

int main(void)
{
    CLINGS_CHECK_INT(classify(1, 1), 1);
    CLINGS_CHECK_INT(classify(1, -1), 0);
    CLINGS_CHECK_INT(classify(-1, 1), 2);
    return clings_report();
}
