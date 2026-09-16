/*
 * clings exercise: 10_aggregates/11_struct_file
 * title: Writing and reading structs
 * objective: Store a struct with fwrite and read it back with fread.
 * hint: Use binary mode and compare the number of complete items written.
 */

#include "clings/test.h"

#include <stdio.h>

struct record {
    int id;
    double value;
};

int write_record(const char *path, const struct record *record)
{
    FILE *file = fopen(path, "wb");
    if (file == NULL) {
        return -1;
    }
    /* TODO: write one complete record. */
    size_t written = fwrite(record, 1, sizeof *record, file);
    if (fclose(file) != 0) {
        return -1;
    }
    return written == 1 ? 0 : -1;
}

int read_record(const char *path, struct record *record)
{
    FILE *file = fopen(path, "rb");
    if (file == NULL) {
        return -1;
    }
    size_t read_count = fread(record, sizeof *record, 1, file);
    fclose(file);
    return read_count == 1 ? 0 : -1;
}

int main(void)
{
    const char *path = "/tmp/clings_struct_file_test.bin";
    struct record written = {.id = 7, .value = 3.5};
    struct record read_back = {0};

    CLINGS_CHECK_INT(write_record(path, &written), 0);
    CLINGS_CHECK_INT(read_record(path, &read_back), 0);
    CLINGS_CHECK_INT(read_back.id, 7);
    CLINGS_CHECK_INT(read_back.value == 3.5, 1);
    remove(path);
    return clings_report();
}
