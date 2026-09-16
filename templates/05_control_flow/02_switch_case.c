/*
 * clings exercise: 05_control_flow/02_switch_case
 * title: switch and fallthrough
 * objective: Use intentional fallthrough and a default case.
 * hint: February has 29 days when leap is true.
 */

#include "clings/test.h"

int days_in_month(int month, int leap)
{
    switch (month) {
    case 1:
    case 3:
    case 5:
    case 7:
    case 8:
    case 10:
    case 12:
        return 31;
    case 4:
    case 6:
    case 9:
    case 11:
        return 30;
    case 2:
        /* TODO: account for leap years. */
        return 28;
    default:
        return -1;
    }
}

int main(void)
{
    CLINGS_CHECK_INT(days_in_month(1, 0), 31);
    CLINGS_CHECK_INT(days_in_month(4, 0), 30);
    CLINGS_CHECK_INT(days_in_month(2, 0), 28);
    CLINGS_CHECK_INT(days_in_month(2, 1), 29);
    CLINGS_CHECK_INT(days_in_month(13, 0), -1);
    return clings_report();
}
