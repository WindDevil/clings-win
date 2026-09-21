已经把工程跑通并逐层看完了。先说明一点：这个会话里没有可用的 MCP 资源（`list_mcp_resources` 和 `list_mcp_resource_templates` 都返回空），所以我改成在本机直接驱动运行器和 studio——对"以新生身份体验"这个目标来说反而更直接，因为跑的就是 Learner 真正会跑的那条路径。

---

# 一、这个工程是什么

`clings-win` 是上游 [clings](https://github.com/WindDevil/clings) 的 **Windows 孪生工程**：同一套 185 道 C 练习题，换成 Windows 的入口、工具链和分发包，目标用户是"只用 Windows、机器上什么都没装"的大一学生。

它要解决的其实是一个**分发问题**，不是一个教学问题。练习题本身、测试框架、运行器都来自上游；本仓库只保存三处差异：12 个练习的 Windows 平台变体、运行器的 Windows 适配、以及中英翻译表。`make check` 在 CI 里核对"上游 + 这三处差异"的结果，两边不会各写一份——这个结构选择很关键，它让"同步上游新练习"从"移植工作"降级成"补几条翻译词条"。

 Learner 侧的产品形态：双击 `clings.cmd` → 编译并测试下一道未完成的题 → 失败是故意的（文件里留了 TODO，编译器报错就是题目）→ 菜单里可以重跑 / 用 VS Code 打开 / 用内置网页编辑器 / 看提示。没有"环境配置"这一步，这是它最值钱的地方。

# 二、我实际跑了什么

- `./clings list / run / hint / solution / reset / verify / selftest / doctor / run --all --json`
- `python3 -m studio menu`（走完新生第一次双击的全流程，含欢迎语、跑题、菜单）
- `python3 -m studio web`：起真服务器，用 curl 扮演浏览器打了一遍 API——正常读文件、`/api/check` 真编译、`/api/completion`、`/api/run`，以及一组恶意请求
- `make test`：135 + 16 个测试全绿
- `python3 tools/sync_from_source.py --source ../cling --check`：孪生工程与上游一致（上游 checkout 就在 `../cling`）
- 新生闭环：把 `Hello, world!` 改成 `Hello, C!` → 通过 → `reset` → 回到坏的初始状态

**在本机（Linux，非 Windows 目标）的实测结果：** `verify` 182/185 通过，3 个失败全是 Windows 专有练习（`12_standard_library/11_environment` 用 `_putenv_s`、`17_translation_units/05_dynamic_linking` 用 `windows.h`、`19_modern_c_library/01_noreturn` 用 `process.h`）——这与 `docs/portability.md` 的说明一致，不是缺陷。**我没能跑 Windows 回路**：本机没有 mingw-w64 和 Wine，`make windows-check` 无法执行，所以文档里"185/185 在 Wine 下通过"这条我只能采信、不能复现。

# 三、难度梯度

调整后的排课顺序保持全部练习都在，只改变学习路径：基础 I/O → 预处理 → 类型 → 宏 → 运算符 → 控制流 → 函数 → 指针 → 数组/字符串 → 动态内存 → 聚合 → 数据表示 → 标准库 → 字符/文件 I/O → UB → 数据结构 → 编译单元 → C11 高级特性。知识覆盖按你说的"就覆盖当前这些"来看，广度是够的：从 `printf` 一路到 `_Generic`、`atomic_flag`、`container_of`、arena 分配器、X-macro，几乎没有常见缺口。

但有四个地方梯度不平：

**1. 宏排得太早、太密（已调整位置，不删除练习）。** `02_macros` 改到 `03_types_variables` 之后。学生先学类型宽度、有符号/无符号转换、整型提升，再进入宏；`02_macros/05_x_macros` 的难度尖峰因此有了必要的铺垫。

**2. UB 主题放得太靠后，而 UB 的种子早就埋下了。** `15_ub_safety` 保留全部题目；课程说明在类型、数组和运算符章节分别提前点明 `01_signed_overflow`、`03_out_of_bounds`、`05_sequence_points`，到 UB 单元再系统化总结。这样不删除练习，也不把整组 UB 硬挪到基础章节。

**3. 重复题偏多。** 保留三对真正重复的练习：

| 题 A | 题 B | 重复点 |
| --- | --- | --- |
| `03_types_variables/03_overflow` | `15_ub_safety/01_signed_overflow` | 同为"相加前检测溢出"，连 `INT_MAX, 1` / `INT_MIN, -1` 测试值都一样 |
| `07_pointers/06_dangling_wild` | `15_ub_safety/04_use_after_free` | 同为 `free(*p)` 后通过二级指针置 NULL，连 `is_null` 辅助函数都一样 |
| `07_pointers/02_null_and_const` | `15_ub_safety/08_null_pointer` | 同为"NULL 就不解引用" |
学生连做两遍同一件事，第一遍的新鲜感会变成"这题我做过"。其中有界拷贝和 `strncpy` 一对虽然主题相近，但教学目标不同，保留两题，不再把它重复计入“需要删题”的清单。

**4. `16_data_structures` 题量最少而跨度最大。** 现有三题保留，运行器中的顺序改成“环形队列 → 动态数组 → 二叉查找树”；更早的 `09_dynamic_memory/07_linked_list` 作为链式结构过渡，BST 的提示按“先完成右子树插入，再验证查找”两个检查点阅读，补上从线性结构到树结构的中间难度。

另外 `13_character_io` 和 `12_standard_library` 有重叠：`12_standard_library/14_ctype_full` 和 `13_character_io/06_include_ctypes` 讲同一块 `<ctype.h>` 知识，而 `03_types_variables/05_char_ascii` 也已经用过 ctype 了。

# 四、合理性

设计取舍整体非常清楚，而且几乎每个都能在代码注释里找到"为什么这样做而不是那样做"：

- **孪生工程而非 fork**：练习内容唯一事实来源在上游，Windows 只留差异表。这让"上游加了练习"从移植变成补翻译。
- **运行器零依赖**（Python 标准库 + 一个 C 编译器）：这是对"第一个障碍是环境配置"这个判断的正确回应。
- **内置编辑器用编译器做语法检查，不解析 C**：`studio/languages/c.py` 把缓冲区写进临时目录，用 `run` 的同一套参数跑 `-fsyntax-only`。注释里写得很直白：一个近似的检查器比没有更糟，因为学员会信它。这是我对整个工程评价最高的一处设计。
- **双击先跑题再给菜单**，而不是打印一份滚过去的清单——对"窗口一闪就没"这个真实场景的判断是对的。
- **`clings.cmd` 的暂停规则宁可多按一次键**：因为两种错误的代价不对称（一次按键 vs 窗口在读到第一行前关掉）。
- **`.\clings.cmd` 而不是 `clings.cmd`**：PowerShell 不搜当前目录，这是实测过的。

有两处我认为值得再想：

- **`solutions/` 随分发包发给学生**，而且 `clings.cmd solution <题>` 是正式命令。对自学工具这是合理取舍，但它和"先看编译器输出再看答案"的教学主张有张力。rustlings 的做法是把答案放在单独的目录、且不进发布包。如果担心抄答案，可以在 `progress.json` 里记一下"看过答案的题"，让进度条的含义保持诚实。
- **full 包 190 MB vs slim 包 0.6 MB**：分两个包是对的，但"已经装了 Python 3 和 MinGW-w64 GCC 的人"这个画像，和"双击 `clings.cmd` 的新生"重叠度有多高，我存疑。更常见的中间态是"装了 Python 但没装编译器"——这种情况两个包都不太合适。

# 五、严谨程度

这套工程在严谨性上明显高于同类教学项目，具体表现在：

**测试策略。** `clings selftest` 检查的不变量是"参考答案通过 **且** 初始状态必须失败"——这一个测试就钉住了整个教学法的前提，而且它跑在 CI 里。`make test` 的 151 个测试用的是真运行器、真编译器、真练习题，注释里写"a stub would only agree with itself"（打桩只会和它自己一致），并且 `harness.unchanged()` 会把练习文件和 `progress.json` 字节级还原，免得测试把生成树改脏导致 `make check` 误判。

**平台差异的硬契约。** `windows_overrides.py` 和 `sync_from_source.py` 的每一处替换都要求"精确命中一次，否则直接报错"。上游一改那几行，同步就失败并告诉你缺哪几条——不会悄悄生成一份坏树。翻译层同样：英文命中不到中文词条就报错并列出缺的句子。

**CRLF 这个坑是被认真对待的。** 生成物一律 `write_bytes` 而不是 `write_text`，因为文本模式会把 `\n` 翻成 `os.linesep`，在 Windows 上会让整棵树每行多一个字节、`--check` 把每个文件都报成 `differs`。`.gitattributes` 把 `*.cmd` 定为 CRLF（`file clings.cmd` 确认工作区是 CRLF，git blob 里是 LF），打包时再归一化。这一层是很多项目会漏的。

**内置编辑器的安全模型是完整闭环的。** 我实测验证过：只绑 `127.0.0.1`；一次性令牌 + `Origin` 双重校验（错误的端口返回 403）；`paths.resolve_within` 用 `resolve()` 折叠 `..`、跟随符号链接、归一化 Windows 大小写，越界一律拒；文件读写还被第二道闸限制在"运行器列出的属于这个练习的文件"内，所以连 `clings` 自己、`progress.json`、`README.md` 都写不进去；`MAX_BODY` 限体量；CSP 是 `default-src 'none'; script-src 'self'`，没有 `unsafe-eval`；前端除了渲染包内自带的 README 之外全部走 `textContent`。它也不是沙箱——注释明说"编辑器跑的就是 `run` 跑的那个编译器"，这个边界划得诚实。

**文档是实测出来的，不是猜的。** 控制台颜色那段附了在真机上往 `CONOUT$` 写转义再读回屏幕缓冲的模式对照表（`0x4`/`0x6` 不够，`0x5`/`0x7` 才行），并且指出 `isatty()` 为真不等于控制台会解释转义——这正是上游踩的坑。`._pth` 那段写明了 full 包 v0.3.0 是怎么发坏的、slim 包为什么恰好没事。

**反馈分层（T0–T4）** 也是想清楚了才写的：交叉编译 → Wine → 真 Windows CI → 人工冒烟，并且明确说 QEMU 性价比低、不要上。

严谨性上的缺口：

- **Linux 上 `make test` 不覆盖练习题本身。** 它只跑 studio 和打包的测试，`verify`/`selftest` 只在 `windows-check` 里，而那个需要 winbox。一个没有 Wine 的 Linux 贡献者跑 `make test` 全绿，但对练习题的状态一无所知。studio 测试里确实有几条通过 bridge 间接碰了运行器（`test_the_listing_is_complete`、`test_a_solution_is_source_text`），算是部分补偿。
- **MSVC 链路没进 CI**，文档里关于 MSVC 的结论是推断而非实测——这点它自己承认了。
- **`exercise.reference` 这个元数据字段从来没有被填充过**，运行器里 `print_exercise` / `command_hint` / `exercise_record` 三处都为它写了分支。要么补上参考资料（对自学工具其实很有用），要么删掉这个死分支。
- **`docs/provenance.md` 的 "windows overrides: 12" 是生成出来的人工数字**，和 `windows_overrides.rewritten_exercises()` 一致，没问题；但它和 README 里"12 个练习需要平台变体"是两处手抄，改一处容易漏另一处。

# 六、具体问题清单

按严重程度排：

**会直接影响新生的（1 处）**

1. **多文件练习的"要改的文件"指错了（已修复）。** `next_steps()` 现在从练习实际参与编译的文件中筛出含 `TODO` 的文件；没有 TODO 时才回退到全部文件。因此 `17_translation_units/02_extern_linkage` 会指向 `config.c`，`03_static_internal_linkage` 会指向 `counter.c`，CLI、studio 两个入口不再互相矛盾。

**维护性 / 一致性（3 处）**

2. `studio/web/app.js` 的完成文案已改为读取 `/api/session.total`，不再硬编码 `185`。
3. `tools/zh_translate.py` 的 `rewrite()` 已删除未使用的 `strict` 参数；严格模式仍由 `main()` 统一处理。
4. `server.py` 的 `_State.origin` 现在显式为 `None`，只在服务绑定端口后进行 Origin 比对；忘记注入端口时不会构造一个错误的默认 Origin。

**行为副作用（1 处）**

5. `clings run --all` 会把 Linux 上"意外通过"的练习写进进度（已修复）。全量运行现在只报告结果，不写入 `.clings/progress.json`；单题运行仍按原逻辑记录完成状态。

**排课（4 处，见第三节）**：宏前置、UB 种子解释滞后、三对重复题、`16_data_structures` 跨度。

**一个我没能验证的边界**：`clings.cmd` 用 `%ROOT%` 拼接 PATH，如果解压路径里含 `%`（比如 `C:\clings\%test%\`），cmd 会把它当变量展开。冒烟清单用的 `C:\Users\测试 用户\桌面\clings win\` 覆盖了空格和中文，没覆盖 `%`。概率极低，但如果想稳，可以在 `set "PATH=..."` 之前加一句 `set "ROOT=%ROOT:%=%%%"` 之类的转义，或者在文档里明说路径里不要有 `%`。

# 七、总结

这是一份**工程质量明显超出"教学练习集"平均水平**的工作。它的强项不在练习题本身（那来自上游），而在于把一个"只在 POSIX 上成立"的东西搬到 Windows 时，把每一个会炸的地方都找出来、量出来、写下来，并且用"精确命中一次的补丁 + CI 核对"保证它不会悄悄腐坏。控制台颜色那两个模式位、embeddable Python 的 `._pth`、`write_bytes` 对抗 CRLF——这三件事任何一件都足以让一个 Windows 分发包在学员机器上死掉，而它三件都抓住了，还各自留了文档和测试。

作为大一学生的体验也是成立的：我第一次双击看到的是"这个包里有 185 道题、每道题都留了一处空、报错就是线索、不是环境装坏了"，这四句话对的人是决定性的——大部分人在第一份 `error:` 面前会先怀疑自己装错了东西。

最值得保留的两项改动是：**把多文件练习的"要改的文件"指对**，以及**重排难度梯度**（宏后移、UB 种子就近回顾、用链表和动态数组填补队列到 BST 的跨度）。前者已经落地，后者不删除练习，只调整学习顺序和提示检查点。
