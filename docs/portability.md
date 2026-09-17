# Windows 可移植性

本文记录 `clings` 在 Windows 目标下的实测结果、必须修改的练习，以及在没有
Windows 机器的前提下如何获得闭环反馈。

## 结论

185 个练习里只有 12 个需要 Windows 变体，其余原样可用。因此孪生工程采用
「同步 + 覆盖表」结构，而不是维护两套练习。

## 实测数据

在 Linux（无 Windows、无 KVM）上用 `x86_64-w64-mingw32-gcc` 交叉编译全部
参考答案，并在 Wine 9.0 中执行：

| 阶段 | 结果 |
| --- | --- |
| 未修改的上游代码编译 | 181 / 185 |
| 未修改的上游代码运行 | 180 / 181（补齐 `libwinpthread-1.dll` 后） |
| 应用 Windows 覆盖后编译 | 185 / 185 |
| 应用 Windows 覆盖后运行 | 185 / 185 |
| 初始练习仍然失败（`selftest`） | 185 / 185 |

真实数字由 `make windows-check` 每次重新产出，不要手抄。

## 覆盖表

| 练习 | 上游写法 | 问题 | Windows 变体 |
| --- | --- | --- | --- |
| `03_types_variables/01_integer_types` | `(long)INT_MAX + 1L` | Windows 是 LLP64，`long` 只有 32 位，表达式溢出，`-Werror=overflow` 直接编译失败 | 只在 `sizeof(long) > sizeof(int)` 时取下一个值，并在 `else` 分支断言 `sizeof(long) == sizeof(int)`，把数据模型差异变成学习点 |
| `12_standard_library/11_environment` | `setenv` / `unsetenv` | POSIX 接口，MSVCRT/UCRT 没有 | `_putenv_s(name, value)` / `_putenv_s(name, "")` |
| `12_standard_library/15_rand_max` | 初始代码 `RAND_MAX == 32767` | 这个破绽在 glibc 上不成立（`RAND_MAX` 是 2147483647），但在 Microsoft CRT 上恰好为真，练习会一开局就通过 | 只改初始练习和模板：`RAND_MAX > 32767`，保留「保证的最小值是闭区间」这一教学点 |
| `13_character_io/02_eof_ferror` | `CLINGS_CHECK_INT(feof(f), 1)` | Microsoft CRT 的 `feof` 返回内部标志（`0x10`），不是 1 | 断言改为 `feof(f) != 0` |
| `17_translation_units/05_dynamic_linking` | `dlopen` / `dlsym` / `dlclose` | POSIX 动态加载，Windows 没有 `dlfcn.h` | `LoadLibraryA` / `GetProcAddress` / `FreeLibrary`，库名换成 `msvcrt.dll` |
| `19_modern_c_library/01_noreturn` | `fork` / `waitpid` | Windows 没有 `fork` | 子进程改为「用 `child` 参数重新执行自己」+ `_spawnv` / `_cwait` |
| 6 个写临时文件的练习（`00_basics/03_scanf`、`10_aggregates/11_struct_file`、`12_standard_library/07_file_io`、`14_file_io/01`、`06`、`07`） | 绝对路径 `"/tmp/clings_*.txt"` | Windows 上 `/tmp/x` 指 `D:\tmp\x`，该目录不存在，`fopen` 直接返回 NULL | 改成相对文件名，落在工作目录里；测试末尾照旧删除 |

最后一行是上线前最后一次真 Windows CI 抓到的：在 Wine 和 Linux 上全都通过，
只有真机才暴露出来。

临时文件改成相对路径后，学员的代码如果崩在中途，会在工作目录里留下
`clings_scanf_valid.txt` 这类文件。`03_scanf` 的测试会在开头先清理上一次的
残留，所以只要修好代码再跑一次就会消失。

覆盖实现在 [`tools/windows_overrides.py`](../tools/windows_overrides.py)。替换要么
精确命中一次，要么直接报错，所以上游一改动这里就会失败而不是悄悄生成错误代码。

## 中文注释

练习的标题、目标、提示、注释和命令行输出由
[`tools/zh_glossary.py`](../tools/zh_glossary.py) 翻译，`make sync` 的最后一步
把译文刷进生成树。术语表按「英文原文 → 中文」组织，命中不到就报错，所以上游
加了一个练习而没补词条时，同步会失败并列出缺的那几句，不会留下半句英文。

标识符、函数名、格式说明符、`TODO:` 前缀和命令保持英文：新手要在报错信息、
教材和 Stack Overflow 之间对照，翻译这些只会增加噪音。

唯一的例外是 20 个主题页里的 `./clings run <slug>`：那是写给 POSIX 读者的，
而 cmd.exe 会把开头的 `./` 当成一个叫 `.` 的命令，直接报"不是内部或外部命令"。
翻译层把它改写成 `.\clings.cmd run <slug>`，围栏标记也从 `sh` 改成 `bat`，
和本工程 README 的写法一致（见 `tools/zh_translate.py` 里的 `windows_command`）。

开头的 `.\` 不是随手加的：**两个 Windows shell 只有这一种写法都能用**。

| 写法 | cmd.exe | PowerShell |
| --- | --- | --- |
| `./clings` | 报"不是内部或外部命令" | 报"不是内部或外部命令" |
| `clings.cmd` | 能用（默认设置下 cmd 会先找当前目录） | 报"无法将…识别为 cmdlet" |
| `.\clings.cmd` | 能用 | 能用 |

裸 `clings.cmd` 在 PowerShell 里必失败，因为 PowerShell 从不搜索当前目录；
在 cmd 里能不能用则取决于 `NoDefaultCurrentDirectoryInExePath`——设了这个环境
变量（不少加固过的机器会设）之后同样失败。运行器在所有练习做完后提示的那句
`verify` 走的也是同一个 `launcher()`。

翻译过程中发现的两个 Windows 细节：

- `chcp 65001` 只切换控制台，Python 仍然按控制台代码页编码 stdout，在
  非中文 Windows 上打印中文会直接抛 `UnicodeEncodeError`。运行器里加了
  `configure_output()` 把 stdout/stderr 重设为 UTF-8（并把错误降级成 `?`），
  `clings.cmd` 同时设置 `PYTHONUTF8` 和 `PYTHONIOENCODING`。
- 这个崩溃只有在「解压后的完整包 + 自带 Python」下才会出现，Linux 上的
  `clings verify` 永远碰不到。它属于 T1 回路该抓的问题。

## 控制台颜色

上游的运行器用 ANSI 转义序列上色（`\033[36mrunning\033[0m`，本工程译作
`\033[36m运行\033[0m`）。Linux 终端默认解释这些转义，Windows 控制台**不会**：
进程必须打开控制台输出模式里的**两个**位——`ENABLE_VIRTUAL_TERMINAL_PROCESSING`
和 `ENABLE_PROCESSED_OUTPUT`——否则 conhost 把转义当成普通字符存进屏幕缓冲区，
学员看到的就是 `?[36m运行?[0m` 这种噪声。

这不是猜测，是在真 Windows 控制台上量出来的（往 `CONOUT$` 写一行带转义的文本，
再用 `ReadConsoleOutputCharacter` 读回来）：

| 控制台模式 | 屏幕缓冲区里实际存的内容 |
| --- | --- |
| `0x3` / `0x4` / `0x6`（缺 `ENABLE_PROCESSED_OUTPUT`） | `'Q\x1b[36mXY\x1b[0mZ'`（原样存下，屏幕上就是噪声） |
| `0x5` / `0x7`（两个位都有） | `'QXYZ'`（转义被解释，颜色生效） |

`ENABLE_PROCESSED_OUTPUT` 这个位容易漏：只打开 VT 位是不够的，`0x4` 和 `0x6`
都把转义原样留在缓冲区里。而全新控制台的模式是 `0x3`，在它上面 `| 0x5` 之后
恰好两个位都有，于是"随手试一下能用"会把差别掩盖过去——上游那句
`sys.stdout.isatty()` 就是踩在这里：isatty 为真不等于控制台会解释转义。
`clings` 因此两个位都显式检查、显式设置。

因此运行器的 `color()` 换成了一套显式策略：

- `CLINGS_COLOR=always` / `never` 优先，用来自动化测试和"猜错了"的学员；
- 其次是通行的 `NO_COLOR`（<https://no-color.org/>）；
- 然后是自动判断：不是终端就关颜色；是终端就调用一次
  `GetConsoleMode` / `SetConsoleMode`，控制台不接受 ANSI 时**退回纯文本**，
  而不是把转义码打到屏幕上。`GetConsoleMode` 失败说明这个句柄根本不是
  Windows 控制台（重定向到文件、`NUL` 这类字符设备、或者管道式伪终端），
  没有 conhost 需要说服。

三个容易记错的细节，都在真机上量过：

- **ConPTY 之下的 mintty 走得通**：原生 Windows Python 在那里 `isatty()` 为真、
  `GetConsoleMode` 成功且模式已经是 `0x7`（VT 已开），所以走的是"已经支持"
  那条分支，而不是上面的失败分支。
- **管道式伪终端（Git Bash 默认路径）根本没有颜色**：那里的 stdout 连
  `isatty()` 都是假，运行器按"输出不是终端"关闭颜色，`doctor` 会这么说。
  想在 Git Bash 里看颜色，用 `CLINGS_COLOR=always`——不要指望自动判断，
  它优先相信 `isatty()`。
- **颜色模式属于屏幕缓冲区，不属于进程**：`SetConsoleMode` 打开的两个位会被
  同一个窗口里的其它程序继承，并且在 `clings` 退出后仍然有效（`git`、`gcc`
  这些程序同样如此）。所以 `clings` 只负责打开，不负责还原。

`clings doctor` 会打印当前判断和原因，用来确认"这一台机器到底走的是哪条路"：

```text
颜色:     开启
颜色:     关闭（控制台不支持 ANSI）
```

## 双击入口

`clings.cmd` 是手写的（不在生成物之列），做四件事：找到 Python、把 `runtime\`
加进 `PATH`、按参数转交给运行器或 `studio`、在该暂停的时候暂停。

不带参数时它**先跑下一个未完成的练习，再给菜单**，而不是打印一份清单：双击是
新手唯一的入口，而"快速弹一个窗口又关掉"的教学价值是零。命令行用法不受影响——
任何参数都照旧直达运行器，`clings.cmd run` 的行为一个字没变。

暂停的判断只有一条规则：`%cmdcmdline%` 里出现脚本名就暂停。

| 启动方式 | `%cmdcmdline%` 里有什么 | 结果 |
| --- | --- | --- |
| 双击（Explorer 的文件关联） | `cmd /c ""D:\...\clings.cmd" "` | 暂停——窗口本来会随进程一起消失 |
| PowerShell 里 `.\clings.cmd web` | `cmd.exe /c ""D:\...\clings.cmd""` | 暂停——**多余**，那个窗口不会消失 |
| 已打开的 cmd.exe 里 `.\clings.cmd web` | 只有 `cmd.exe` 自己的路径 | 不暂停 |

第二行是在真机上量出来的（Windows 10 19045）：PowerShell 也经由 `cmd /c`
启动，命令行里同样有脚本名，所以这条规则**分不出**它和双击。两种判断错误的
代价不对称——多按一次键，和窗口在学员读到第一行字之前关掉——所以宁可多按一次。

只有 `open`、`web`、`menu` 和「不带参数」这四条路会走到暂停；其余参数直接转交运行器
（`run`、`list`、`doctor`），把控制台原样交还给调用者，从哪个 shell 调用都一样。

`.\clings.cmd` 这个写法本身的原因见上一节：它是两个 Windows shell 唯一都认的
一种拼法。Python 的查找顺序是包内 `runtime\python\python.exe` → `py -3` →
`PATH` 上的 `python`，都没有就打印安装提示并暂停（这里**必须**暂停，否则双击
看到的还是一闪而过）。

## 内置编辑器（`studio\`）

内置编辑器是一个可选的目录，**删掉它练习照样能跑**（冒烟清单第 22 步验证这
一点）：运行器不知道它存在，它也只通过运行器的命令行接口说话。

| 关注点 | 做法 |
| --- | --- |
| 去耦 | `studio/bridge.py` 是唯一和运行器说话的地方（`list`/`doctor`/`run` 走 `--json`，`solution`/`reset` 原样调用）；不 import 运行器，不解析人类可读输出，不另存一份"练习在哪、里面有什么" |
| 数据来源 | `--json` 是 `RUNNER_PATCHES` 加进生成运行器的，属于运行器的接口而不是 studio 的——任何 shell 都能用，不需要 Python 以外的依赖 |
| 语言 | 语言是插件（`studio/languages/`）：`plain.py` 什么也不答，所以编辑器不是 C 专用的；`c.py` **不解析 C**，它把缓冲区写进临时目录，用 `run` 编译这个练习时的同一套参数跑 `-fsyntax-only`，编辑器的报错于是不可能和 `run` 打架；没有编译器时它只说"去跑 doctor"，不猜 |
| 前端 | 无构建步骤，打开就是源码；`studio/web/vendor/` 里是 CodeMirror 5.65.16 和 marked 4.3.0（都是 MIT） |
| 安全 | 只监听 `127.0.0.1`；页面注入一次性令牌，接口另外校验 `Origin`；文件读写被限制在运行器列出的文件清单内；CSP 为 `script-src 'self'`、无 `unsafe-eval` |
| 测试 | `make test`；`windows.yml` 的 `real-windows` job 和 `release.yml` 都会跑它，`studio/tests` 不打进分发包——它需要 checkout 才有意义，而且会改写练习 |

## 维护工具在 Windows 上

`tools/` 里的生成脚本原先用 `Path.write_text()` 写文件，它默认把 `\n` 翻译成
`os.linesep`，所以在 Windows 上生成的整棵树比上游多一个字节/行，
`sync_from_source.py --check` 会把每个文件都报成 `differs`——`make check`
在 Windows 上等于永远失败，只有 Linux CI 能给出真话。

写生成物的地方现在一律走 `Path.write_bytes(text.encode("utf-8"))`。不用
`write_text(..., newline="\n")` 是为了兼容：`newline=` 参数 Python 3.10 才有，
而维护者用的是自己机器上的 Python。`write_bytes` 没有换行翻译这一步，从
Python 3.8 到 3.13 行为一致，也就没有"在新 Python 上绿、在旧 Python 上红"
的可能。Windows 上的 `make check` 和 CI 结论一致。

## 发布包

`make package` 产出两个 zip，对应两种真实情况：

| 包 | 内容 | 大小 | 面向 |
| --- | --- | ---: | --- |
| `-full.zip` | 练习 + 内置编辑器 + w64devkit + 嵌入式 Python | 约 190 MB | 机器上没有任何开发工具的人 |
| `-slim.zip` | 只有练习 + 内置编辑器 | 约 0.6 MB | 已经有 Python 3 和 MinGW-w64 GCC 的人 |

文件名里的 `<commit>` 是**本仓库**的 commit。早先用的是上游 commit，结果每次重建
（包括修掉控制台颜色那次）都和上一个坏包同名，下载目录里两个不同的 zip 重名，
分不出哪个是修好的。

上游 commit 只记在 `docs/provenance.md` 和包内的同一份文件里——**Release 说明里
没有**。说明正文是 `release.yml` 里写死的 `body:`，每次发布都一模一样，不会跟着
commit 走；包名改用本仓库 commit 之后，上游 commit 在 Release 页面上就不再出现了。
要核对上游版本，看 `docs/provenance.md`，别看 Release 页面。

打 tag（`v*`）会触发 [`.github/workflows/release.yml`](../.github/workflows/release.yml)：
在真 Windows runner 上先 `verify` + `selftest`，再拉取 w64devkit 和 Python 打进
full 包，最后把两个 zip 挂到 GitHub Release。

## 保持可移植的写法

新增练习时，下列写法在 MinGW-w64 下可直接使用：

- `pthread.h`、`_Thread_local`：需要 `-pthread`，并随程序分发
  `libwinpthread-1.dll`（这是 Windows 的 DLL 部署问题，不是代码问题）。
- `strtok_r`、`stdatomic.h`、`complex.h`、`tgmath.h`、VLA、
  `__builtin_frame_address`、`%zu`：MinGW-w64 全部支持。
- 避免 `setenv` / `unsetenv` / `dlopen` / `fork` / `sys/wait.h` / `unistd.h`
  里的进程接口；这些是 POSIX 专有。
- MSVC 不支持的更多：VLA、`complex.h`、`tgmath.h`、`__builtin_frame_address`，
  以及 `strtok_r` 的签名。这也是本工程把 MinGW-w64 作为主工具链的原因：
  MSVC 需要额外安装 3–6 GB 的 VS Build Tools 且要求管理员权限，对新手门槛过高。

## 无 Windows 的闭环反馈

| 层级 | 手段 | 覆盖什么 | 代价 |
| --- | --- | --- | --- |
| T0 | mingw-w64 交叉编译 | 头文件、类型宽度、告警（与上游同一套 `-Werror`） | 秒级 |
| T1 | Wine 9 运行 PE | 运行时语义、CRT 差异、DLL 依赖 | 秒级 |
| T2 | GitHub `windows-latest` | 真 Windows + 真 MinGW，打包产物 | 分钟级，免费 |
| T3 | 人工冒烟（[清单](windows-smoke-test.md)） | 双击体验、SmartScreen/Defender、中文控制台、中文路径 | 每次发布 10 分钟 |
| T4 | QEMU 全量虚拟机 | 无人值守的真机 GUI 回归 | 需 KVM；无 KVM 时是纯软件模拟，冷启动 5–15 分钟，性价比低 |

QEMU 只在 T2 和 T3 都不适用（离线、需要 GUI 截图或录屏）时才值得上。真 Windows
的正统回路是 CI runner，真实性的回路是人。

本仓库的 T0/T1 由 `tools/winbox.sh` 提供：它把 mingw-w64 交叉编译器和 Wine 解包
到 `.winbox/`，不需要 root、不往系统里装任何东西。它同时修复了 Ubuntu wine64
包在重定位后必定踩到的两个坑（`wineserver` 包装脚本写死绝对路径、`user32.dll`
依赖的 `zlib1.dll` 被装在 mingw sysroot 里）。

## 已知差距

- MSVC（`cl.exe`）链路尚未进入 CI 矩阵，上面的 MSVC 结论来自文档而非实测。
- `clings.cmd` 的暂停规则分不出双击和 PowerShell，后者会多按一次键（原因和取舍
  见「[双击入口](#双击入口)」）。`%cmdcmdline%` 里那条尾随空格的差别来自文件
  关联模板，不是稳定契约，因此没有拿它做判断。
- `studio` 的测试只在 Windows runner 和真机上跑；Linux 上的 T0/T1 回路
  （`make windows-check`）覆盖的是运行器，不覆盖 `studio\`。
- `clings.cmd` 无法在 Wine 下验证：Wine 的 `cmd.exe` 需要真正的控制台，在无终端
  的环境里静默不执行。因此该脚本由 `real-windows` job 里的
  `cmd /c clings.cmd doctor` 以及人工冒烟清单覆盖。
- Wine 回路里 `wine` 每次冷启动约 4 秒，脚本用「预热 + 后台保活」把整轮压到
  一分钟以内；如果保活被环境杀掉，回路仍然正确，只是慢。
