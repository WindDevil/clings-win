/*
 * clings exercise: 11_data_representation/05_endianness
 * title: Endianness
 * objective: Detect byte order and inspect an integer's first byte.
 * hint: A uint16_t value of 1 stores 0x01 first on little-endian systems.
 */

#include "clings/test.h"

#include <stdint.h>
#include <string.h>

int is_little_endian(void)
{
    uint16_t value = 1;
    unsigned char bytes[2];
    memcpy(bytes, &value, sizeof bytes);
    return bytes[0] == 1;
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
