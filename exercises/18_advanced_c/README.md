# 高级 C

运行练习：

```bat
clings.cmd run 01_variadic
```

| 练习 | 目标 |
| --- | --- |
| `01_variadic` | 用 va_list 读取数量不定的 int 实参。 |
| `02_setjmp_longjmp` | 用非局部跳转实现一条简单的错误路径。 |
| `03_pthreads` | 创建线程，并用互斥量保护共享状态。 |
| `04_atomics` | 用 atomic_int 做无锁的计数更新。 |
| `05_generic` | 根据值的类型选择对应的表达式。 |
| `06_static_assert` | 用 _Static_assert 在编译期强制检查假设。 |
| `07_align` | 查询对齐，并指定对齐。 |
| `08_anonymous_union` | 通过外层结构体直接访问匿名联合体的成员。 |
| `09_thread_local` | 用 _Thread_local 让每个线程拥有自己的对象。 |
| `10_complex` | 使用 double complex、I、conj、creal 和 cimag。 |
| `11_signal` | 安装信号处理函数，并使用 sig_atomic_t 标志。 |
| `12_stack_frame` | 观察嵌套函数调用使用各自独立的活动记录。 |
