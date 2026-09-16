# 宏与宏卫生

运行练习：

```sh
./clings run 01_object_macro
```

| 练习 | 目标 |
| --- | --- |
| `01_object_macro` | 使用一个有名字的编译期常量。 |
| `02_function_macro` | 用括号保护宏参数和整个展开结果。 |
| `03_stringize_paste` | 用 # 做字符串化，用 ## 拼接记号。 |
| `04_variadic_macros` | 把可变实参列表转发给另一个变参函数。 |
| `05_x_macros` | 用同一份列表生成枚举和字符串表。 |
| `06_macro_whitespace` | 记住一个空格就能把函数式宏变成对象式宏。 |
| `07_macro_statement` | 用 do { ... } while (0) 写像语句一样的宏。 |
| `08_macro_not_typedef` | 指针类型用 typedef，不要用对象式宏。 |
| `09_macro_side_effects` | 看清函数式宏可能多次计算它的实参。 |
| `10_assert_macro` | 程序员错误用 assert，用户错误用返回值。 |
| `11_macro_multiline` | 把宏定义续写到下一行。 |
