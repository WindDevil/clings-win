/*
 * clings exercise: 09_dynamic_memory/06_flexible_array
 * title: Flexible array members
 * objective: Allocate a struct plus trailing data in one block.
 * hint: The allocation size is sizeof *packet + length bytes.
 */

#include "clings/test.h"

#include <stdlib.h>
#include <string.h>

struct packet {
    size_t length;
    unsigned char data[];
};

struct packet *packet_create(size_t length, const unsigned char *data)
{
    struct packet *packet = malloc(sizeof *packet + length);
    if (packet == NULL) {
        return NULL;
    }
    /* TODO: record the payload length. */
    packet->length = 0;
    memcpy(packet->data, data, length);
    return packet;
}

void packet_destroy(struct packet *packet)
{
    free(packet);
}

int main(void)
{
    const unsigned char payload[] = {1, 2, 3, 4};
    struct packet *packet = packet_create(4, payload);

    CLINGS_CHECK(packet != NULL);
    CLINGS_CHECK_INT(packet->length, 4);
    CLINGS_CHECK_INT(packet->data[0], 1);
    CLINGS_CHECK_INT(packet->data[3], 4);
    packet_destroy(packet);
    return clings_report();
}
