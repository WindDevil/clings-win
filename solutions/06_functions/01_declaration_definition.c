/*
 * clings 练习: 06_functions/01_declaration_definition
 * title: 声明与定义
 * objective: 使用前置声明和内部辅助函数。
 * hint: 声明承诺了函数签名，定义提供函数体。
 */

#include "clings/test.h"

static int square(int value);

int square_then_add(int value, int addend)
{
    return square(value) + addend;
}

static int square(int value)
{
    return value * value;
}

int main(void)
{
    CLINGS_CHECK_INT(square_then_add(3, 4), 13);
    CLINGS_CHECK_INT(square_then_add(-2, 1), 5);
    return clings_report();
}
