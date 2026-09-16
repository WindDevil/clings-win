# 结构体、联合体、枚举与位域

运行练习：

```bat
clings.cmd run 01_struct_basics
```

| 练习 | 目标 |
| --- | --- |
| `01_struct_basics` | 创建结构体值，并通过指针访问它的成员。 |
| `02_nested_structs` | 通过外层结构体指针访问嵌套成员。 |
| `03_padding_alignment` | 用 offsetof 观察填充和成员偏移。 |
| `04_bitfields` | 把几个小标志位存进一个结构体。 |
| `05_union` | 比较联合体大小与它最大成员的大小。 |
| `06_enum` | 用枚举表示一小组封闭取值。 |
| `07_typedef_designated` | 使用 typedef，并按名字初始化成员。 |
| `08_container_of` | 由成员指针反推出外层结构体。 |
| `09_struct_array` | 遍历结构体数组，找出最优元素。 |
| `10_struct_pass` | 对比结构体值参数与结构体指针参数。 |
| `11_struct_file` | 用 fwrite 写出结构体，再用 fread 读回来。 |
| `12_complex_declarations` | 读懂并使用函数指针及其数组的 typedef。 |
| `13_declaration_grammar` | 读懂函数指针数组的 typedef。 |
