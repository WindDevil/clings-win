/*
 * clings exercise: 08_arrays_strings/03_multidimensional
 * title: Two-dimensional arrays
 * objective: Transpose a 3x3 matrix with nested loops.
 * hint: The transposed element at [row][column] comes from input[column][row].
 */

#include "clings/test.h"

void transpose3x3(const int input[3][3], int output[3][3])
{
    for (int row = 0; row < 3; ++row) {
        for (int column = 0; column < 3; ++column) {
            output[column][row] = input[row][column];
        }
    }
}

int main(void)
{
    const int input[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9},
    };
    int output[3][3] = {{0}};

    transpose3x3(input, output);
    CLINGS_CHECK_INT(output[0][0], 1);
    CLINGS_CHECK_INT(output[0][1], 4);
    CLINGS_CHECK_INT(output[1][0], 2);
    CLINGS_CHECK_INT(output[1][2], 8);
    return clings_report();
}
