# 动态内存

运行练习：

```bat
.\clings.cmd run 01_malloc_free
```

| 练习 | 目标 |
| --- | --- |
| `01_malloc_free` | 用 malloc 和 free 管理动态长度的数组。 |
| `02_calloc` | 需要每个字节初值都是零时用 calloc。 |
| `03_realloc` | 安全使用 realloc，并只初始化新增的元素。 |
| `04_memory_leak` | 让每次分配都有对应的 free。 |
| `05_buffer_bounds` | 最多复制 dest_size - 1 个字节，并保证结尾有 NUL。 |
| `06_flexible_array` | 用一次分配同时容纳结构体和尾部数据。 |
| `07_linked_list` | 构建、遍历并释放一个链表。 |
| `08_free_then_realloc` | 扩容时直接调 realloc，不要先 free。 |
| `09_arena_allocator` | 实现一个简单的、按对齐分配的区域分配器。 |
| `10_allocation_stats` | 包装 malloc 和 free，跟踪尚未释放的分配。 |
| `11_goto_cleanup` | 用 goto 写出清晰的清理路径。 |
