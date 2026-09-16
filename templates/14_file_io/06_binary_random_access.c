/*
 * clings exercise: 14_file_io/06_binary_random_access
 * title: Binary random access
 * objective: Read a specific struct record from a binary file.
 * hint: Seek by index * sizeof(record).
 */

#include "clings/test.h"

#include <stddef.h>
#include <stdio.h>

struct record {
    int id;
    char name[16];
};

int write_records(const char *path, const struct record *records, size_t count)
{
    FILE *file = fopen(path, "wb");
    if (file == NULL) {
        return -1;
    }
    size_t written = fwrite(records, sizeof *records, count, file);
    fclose(file);
    return written == count ? 0 : -1;
}

int read_record_at(const char *path, size_t index, struct record *out)
{
    FILE *file = fopen(path, "rb");
    if (file == NULL) {
        return -1;
    }
    /* TODO: seek to the selected record. */
    if (fseek(file, (long)index, SEEK_SET) != 0) {
        fclose(file);
        return -1;
    }
    size_t read_count = fread(out, sizeof *out, 1, file);
    fclose(file);
    return read_count == 1 ? 0 : -1;
}

int main(void)
{
    const char *path = "/tmp/clings_binary_records.bin";
    const struct record records[3] = {
        {1, "one"},
        {2, "two"},
        {3, "three"},
    };
    struct record record = {0};

    CLINGS_CHECK_INT(write_records(path, records, 3), 0);
    CLINGS_CHECK_INT(read_record_at(path, 1, &record), 0);
    CLINGS_CHECK_INT(record.id, 2);
    CLINGS_CHECK_STR(record.name, "two");
    remove(path);
    return clings_report();
}
