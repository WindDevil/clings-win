/*
 * clings exercise: 10_aggregates/06_enum
 * title: Enums
 * objective: Use an enum for a small closed set of values.
 * hint: Each case should return the matching color name.
 */

#include "clings/test.h"

enum color {
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE
};

const char *color_name(enum color color)
{
    switch (color) {
    case COLOR_RED:
        return "red";
    case COLOR_GREEN:
        return "green";
    case COLOR_BLUE:
        return "blue";
    default:
        return "unknown";
    }
}

int color_is_valid(int value)
{
    return value >= COLOR_RED && value <= COLOR_BLUE;
}

int main(void)
{
    CLINGS_CHECK_STR(color_name(COLOR_RED), "red");
    CLINGS_CHECK_STR(color_name(COLOR_GREEN), "green");
    CLINGS_CHECK_STR(color_name(COLOR_BLUE), "blue");
    CLINGS_CHECK_INT(color_is_valid(COLOR_BLUE), 1);
    CLINGS_CHECK_INT(color_is_valid(99), 0);
    return clings_report();
}
