/*
 * clings 练习: 13_character_io/03_input_validation
 * title: 输入校验
 * objective: 拒绝带有多余字符或超出范围的输入。
 * hint: 在 %d 后面加 %c，用来发现后面还有非空白字符。
 */

#include "clings/test.h"

#include <stdio.h>

int read_choice(const char *input, int *choice)
{
    int value = 0;
    char extra = '\0';
    /* TODO: 拒绝多余的尾部字符。 */
    if (sscanf(input, "%d", &value) != 1) {
        return -1;
    }
    if (value < 1 || value > 3) {
        return -1;
    }
    *choice = value;
    return 0;
}

int main(void)
{
    int choice = 0;

    CLINGS_CHECK_INT(read_choice("2", &choice), 0);
    CLINGS_CHECK_INT(choice, 2);
    CLINGS_CHECK_INT(read_choice("2x", &choice), -1);
    CLINGS_CHECK_INT(read_choice("9", &choice), -1);
    CLINGS_CHECK_INT(read_choice("abc", &choice), -1);
    return clings_report();
}
