# 未定义行为、安全与可移植性

运行练习：

```sh
./clings run 01_signed_overflow
```

| 练习 | 目标 |
| --- | --- |
| `01_signed_overflow` | 在做有符号加法之前检测溢出。 |
| `02_uninitialized` | 让每个局部变量都有确定的初值。 |
| `03_out_of_bounds` | 拒绝超出逻辑长度的下标。 |
| `04_use_after_free` | 释放目标之后把指针清空。 |
| `05_sequence_points` | 避免对同一对象做无序列点保护的读写。 |
| `06_strict_aliasing` | 用 memcpy 重新解释对象的表示。 |
| `07_alignment` | 用 alignof 查询对齐，并让成员保持对齐。 |
| `08_null_pointer` | 绝不解引用空指针。 |
| `09_standard_changes` | 在编译期判断 C 标准版本。 |
| `10_identifier_length` | 使用较长的内部标识符，并依赖标准给出的最小保证。 |
| `11_implementation_defined` | 观察实现定义的 char 符号性和打包编译指示。 |
