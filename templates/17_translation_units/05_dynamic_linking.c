/*
 * clings 练习: 17_translation_units/05_dynamic_linking
 * title: 用 LoadLibrary 动态加载
 * objective: 在运行时从动态库中取出一个符号。
 * hint: 用 LoadLibraryA、GetProcAddress 和 FreeLibrary；FARPROC 通过联合体转换。
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
    /* TODO: 查找 strlen 这个符号。 */
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
