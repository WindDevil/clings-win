# 编译单元与链接

运行练习：

```sh
./clings run 01_header_source_split
```

| 练习 | 目标 |
| --- | --- |
| `01_header_source_split` | 用 main 文件、头文件和实现文件编译一个程序。 |
| `02_extern_linkage` | 在头文件里声明全局变量，在另一个文件里定义它。 |
| `03_static_internal_linkage` | 用 static 把计数器限制在单个编译单元内。 |
| `04_external_type_check` | 让各个编译单元的声明与定义保持一致。 |
| `05_dynamic_linking` | 在运行时从动态库中取出一个符号。 |
