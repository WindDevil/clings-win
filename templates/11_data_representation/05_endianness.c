/*
 * clings 练习: 11_data_representation/05_endianness
 * title: 字节序
 * objective: 判断字节序，并查看整数的第一个字节。
 * hint: 在小端系统上，值为 1 的 uint16_t 先存 0x01。
 */

#include "clings/test.h"

#include <stdint.h>
#include <string.h>

int is_little_endian(void)
{
    uint16_t value = 1;
    unsigned char bytes[2];
    memcpy(bytes, &value, sizeof bytes);
    /* TODO: 比较 value1 的低字节。 */
    return bytes[0] == 0;
}

int first_byte_of_0x01020304(void)
{
    uint32_t value = 0x01020304u;
    unsigned char bytes[4];
    memcpy(bytes, &value, sizeof bytes);
    return bytes[0];
}

int main(void)
{
    if (is_little_endian()) {
        CLINGS_CHECK_INT(first_byte_of_0x01020304(), 4);
    } else {
        CLINGS_CHECK_INT(first_byte_of_0x01020304(), 1);
    }
    return clings_report();
}
