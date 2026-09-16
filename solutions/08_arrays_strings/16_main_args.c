/*
 * clings exercise: 08_arrays_strings/16_main_args
 * title: argc, argv, and the program environment
 * objective: Work with the arguments passed to main.
 * hint: argv[0] is the program name; user arguments start at argv[1].
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
