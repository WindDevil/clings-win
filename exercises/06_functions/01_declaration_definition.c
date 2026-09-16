/*
 * clings exercise: 06_functions/01_declaration_definition
 * title: Declarations and definitions
 * objective: Use a forward declaration and an internal helper.
 * hint: The declaration promises the signature; the definition supplies the body.
 */

#include "clings/test.h"

static int square(int value);

int square_then_add(int value, int addend)
{
    return square(value) + addend;
}

static int square(int value)
{
    /* TODO: return the square of value. */
    return value + value;
}

int main(void)
{
    CLINGS_CHECK_INT(square_then_add(3, 4), 13);
    CLINGS_CHECK_INT(square_then_add(-2, 1), 5);
    return clings_report();
}
