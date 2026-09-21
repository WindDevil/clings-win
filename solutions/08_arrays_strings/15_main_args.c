/*
 * clings 练习: 08_arrays_strings/15_main_args
 * title: argc、argv 与程序运行环境
 * objective: 处理传给 main 的参数。
 * hint: argv[0] 是程序名；用户参数从 argv[1] 开始。
 */

#include "clings/test.h"

#include <string.h>

int count_user_args(int argc, char **argv)
{
    (void)argv;
    return argc > 0 ? argc - 1 : 0;
}

int find_arg(int argc, char **argv, const char *needle)
{
    for (int i = 1; i < argc; ++i) {
        if (strcmp(argv[i], needle) == 0) {
            return i;
        }
    }
    return -1;
}

int main(void)
{
    char *argv[] = {"program", "--verbose", "file.txt", NULL};

    CLINGS_CHECK_INT(count_user_args(3, argv), 2);
    CLINGS_CHECK_INT(find_arg(3, argv, "--verbose"), 1);
    CLINGS_CHECK_INT(find_arg(3, argv, "file.txt"), 2);
    CLINGS_CHECK_INT(find_arg(3, argv, "missing"), -1);
    return clings_report();
}
