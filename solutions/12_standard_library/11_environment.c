/*
 * clings 练习: 12_standard_library/11_environment
 * title: 环境变量
 * objective: 用 getenv 和 _putenv_s 读写环境变量。
 * hint: _putenv_s 成功之后，getenv 才能找到新值。
 */

#include "clings/test.h"

#include <stdio.h>
#include <stdlib.h>

int set_and_get(const char *name, const char *value, char *out, size_t size)
{
    if (_putenv_s(name, value) != 0) {
        return -1;
    }
    const char *found = getenv(name);
    if (found == NULL) {
        return -1;
    }
    snprintf(out, size, "%s", found);
    return 0;
}

int main(void)
{
    char buffer[32];
    const char *name = "CLINGS_TEST_ENV_VARIABLE";

    CLINGS_CHECK_INT(
        set_and_get(name, "hello", buffer, sizeof buffer), 0);
    CLINGS_CHECK_STR(buffer, "hello");
    _putenv_s(name, "");
    return clings_report();
}
