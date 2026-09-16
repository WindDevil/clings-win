/*
 * clings exercise: 17_translation_units/05_dynamic_linking
 * title: Dynamic linking with LoadLibrary
 * objective: Load a symbol from a shared library at runtime.
 * hint: Use LoadLibraryA, GetProcAddress and FreeLibrary; convert FARPROC through a union.
 */

#include "clings/test.h"

#include <stddef.h>
#include <windows.h>

typedef size_t (*strlen_function)(const char *);

int dynamic_strlen(void)
{
    HMODULE handle = LoadLibraryA("msvcrt.dll");
    if (handle == NULL) {
        return -1;
    }

    union {
        FARPROC object;
        strlen_function function;
    } converter;
    /* TODO: look up the strlen symbol. */
    converter.object = GetProcAddress(handle, "strlen_missing");
    if (converter.function == NULL) {
        FreeLibrary(handle);
        return -1;
    }

    int result = (int)converter.function("hello");
    FreeLibrary(handle);
    return result;
}

int main(void)
{
    CLINGS_CHECK_INT(dynamic_strlen(), 5);
    return clings_report();
}
