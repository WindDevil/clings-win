/*
 * clings 练习: 08_arrays_strings/03_multidimensional
 * title: 二维数组
 * objective: 用嵌套循环转置一个 3x3 矩阵。
 * hint: 转置后 [row][column] 上的元素来自 input[column][row]。
 */

#include "clings/test.h"

void transpose3x3(const int input[3][3], int output[3][3])
{
    for (int row = 0; row < 3; ++row) {
        for (int column = 0; column < 3; ++column) {
            /* TODO: 把行下标和列下标交换。 */
            output[row][column] = input[row][column];
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
