/*
 * clings exercise: 02_macros/05_x_macros
 * title: X-macros
 * objective: Generate an enum and a string table from one list.
 * hint: The string table uses #name, not a fixed string.
 */

#include "clings/test.h"

#define COLOR_LIST(X) X(RED) X(GREEN) X(BLUE)

enum color {
#define X(name) COLOR_##name,
    COLOR_LIST(X)
#undef X
};

static const char *const color_names[] = {
/* TODO: stringize each name. */
#define X(name) "unknown",
    COLOR_LIST(X)
#undef X
};

int main(void)
{
    CLINGS_CHECK_STR(color_names[COLOR_RED], "RED");
    CLINGS_CHECK_STR(color_names[COLOR_GREEN], "GREEN");
    CLINGS_CHECK_STR(color_names[COLOR_BLUE], "BLUE");
    return clings_report();
}
