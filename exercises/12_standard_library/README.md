# 标准库

运行练习：

```bat
.\clings.cmd run 01_printf_formats
```

| 练习 | 目标 |
| --- | --- |
| `01_printf_formats` | 让每个转换说明符与实参类型匹配。 |
| `02_strtol_errno` | 用 strtol、errno 和结束指针校验输入。 |
| `03_qsort_bsearch` | 用比较回调配合排序和查找。 |
| `04_math_functions` | 使用 math.h 里的 hypot 等函数。 |
| `05_time_functions` | 使用 time_t 和 difftime。 |
| `06_random` | 给随机数发生器设种子，并限制输出范围。 |
| `07_memory_functions` | 正确使用按字节操作的内存函数。 |
| `08_string_search` | 使用 strchr、strrchr 和 strstr。 |
| `09_stdint_inttypes` | 使用 stdint.h 和 inttypes.h 里的 uint64_t 与 PRIu64。 |
| `10_environment` | 用 getenv 和 _putenv_s 读写环境变量。 |
| `11_printf_advanced` | 使用宽度、补零、精度和 * 宽度参数。 |
| `12_scanf_advanced` | 在 sscanf 里使用字段宽度和扫描集。 |
| `13_ctype_full` | 把参数转成 unsigned char 后再传给 isalnum 和 toupper。 |
| `14_rand_max` | 不要假定 rand() 的返回值小于某个固定的小上界。 |
