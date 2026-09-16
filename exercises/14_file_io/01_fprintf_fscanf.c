/*
 * clings 练习: 14_file_io/01_fprintf_fscanf
 * title: fprintf 与 fscanf
 * objective: 把格式化数据写入文件，再读回来。
 * hint: 写入和读取用的格式串必须一致。
 */

#include "clings/test.h"

#include <stdio.h>

int write_person(const char *path, const char *name, int age)
{
    FILE *file = fopen(path, "w");
    if (file == NULL) {
        return -1;
    }
    /* TODO: 先写名字，再写年龄。 */
    int ok = fprintf(file, "%d %s\n", age, name) > 0;
    if (fclose(file) != 0) {
        ok = 0;
    }
    return ok ? 0 : -1;
}

int read_person(const char *path, char *name, int *age)
{
    FILE *file = fopen(path, "r");
    if (file == NULL) {
        return -1;
    }
    int ok = fscanf(file, "%31s %d", name, age) == 2;
    fclose(file);
    return ok ? 0 : -1;
}

int main(void)
{
    const char *path = "clings_fprintf_test.txt";
    char name[32];
    int age = 0;

    CLINGS_CHECK_INT(write_person(path, "Ada", 36), 0);
    CLINGS_CHECK_INT(read_person(path, name, &age), 0);
    CLINGS_CHECK_STR(name, "Ada");
    CLINGS_CHECK_INT(age, 36);
    remove(path);
    return clings_report();
}
