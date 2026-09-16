/*
 * clings 练习: 00_basics/03_scanf
 * title: 用 scanf 读输入
 * objective: 用 scanf 从标准输入读一个整数。
 * hint: scanf 需要变量的地址：&value。
 */

#include "clings/test.h"

#include <stdio.h>

int read_number(void)
{
    int value = 0;
    if (scanf("%d", &value) != 1) {
        return -1;
    }
    return value;
}

int main(void)
{
    const char *valid_path = "clings_scanf_valid.txt";
    const char *invalid_path = "clings_scanf_invalid.txt";

    /* 上一轮如果崩溃，先清掉残留的临时文件。 */
    remove(valid_path);
    remove(invalid_path);
    FILE *file = fopen(valid_path, "w");
    CLINGS_CHECK(file != NULL);
    fputs("42", file);
    fclose(file);
    CLINGS_CHECK(freopen(valid_path, "r", stdin) != NULL);
    CLINGS_CHECK_INT(read_number(), 42);

    file = fopen(invalid_path, "w");
    CLINGS_CHECK(file != NULL);
    fputs("abc", file);
    fclose(file);
    CLINGS_CHECK(freopen(invalid_path, "r", stdin) != NULL);
    CLINGS_CHECK_INT(read_number(), -1);

    remove(valid_path);
    remove(invalid_path);
    return clings_report();
}
