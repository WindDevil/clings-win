/*
 * clings exercise: 17_translation_units/04_external_type_check
 * title: External type checking
 * objective: Keep declarations and definitions consistent across translation units.
 * hint: The linker does not compare the types of extern declarations.
 */

#include "clings/test.h"
#include "value.h"

int main(void)
{
    CLINGS_CHECK_INT(shared_value == 3.5, 1);
    return clings_report();
}
