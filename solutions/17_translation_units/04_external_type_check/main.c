/*
 * clings 练习: 17_translation_units/04_external_type_check
 * title: 外部类型检查
 * objective: 让各个编译单元的声明与定义保持一致。
 * hint: 链接器不会比对各个 extern 声明的类型。
 */

#include "clings/test.h"
#include "value.h"

int main(void)
{
    CLINGS_CHECK_INT(shared_value == 3.5, 1);
    return clings_report();
}
