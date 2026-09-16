/*
 * clings 练习: 10_aggregates/04_bitfields
 * title: 位域
 * objective: 把几个小标志位存进一个结构体。
 * hint: 写标志要反映 enabled 参数的值。
 */

#include "clings/test.h"

struct permissions {
    unsigned int read : 1;
    unsigned int write : 1;
    unsigned int execute : 1;
    unsigned int reserved : 29;
};

int flag_enabled(const struct permissions *permissions, int which)
{
    switch (which) {
    case 0:
        return permissions->read != 0;
    case 1:
        return permissions->write != 0;
    case 2:
        return permissions->execute != 0;
    default:
        return -1;
    }
}

void set_flag(struct permissions *permissions, int which, int enabled)
{
    switch (which) {
    case 0:
        permissions->read = enabled ? 1u : 0u;
        break;
    case 1:
        permissions->write = enabled ? 1u : 0u;
        break;
    case 2:
        permissions->execute = enabled ? 1u : 0u;
        break;
    default:
        break;
    }
}

int main(void)
{
    struct permissions permissions = {0, 0, 0, 0};

    set_flag(&permissions, 1, 1);
    CLINGS_CHECK_INT(flag_enabled(&permissions, 1), 1);
    set_flag(&permissions, 1, 0);
    CLINGS_CHECK_INT(flag_enabled(&permissions, 1), 0);
    CLINGS_CHECK_INT(flag_enabled(&permissions, 9), -1);
    return clings_report();
}
