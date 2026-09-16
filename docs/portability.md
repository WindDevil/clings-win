# Windows 可移植性

本文记录 `clings` 在 Windows 目标下的实测结果、必须修改的练习，以及在没有
Windows 机器的前提下如何获得闭环反馈。

## 结论

185 个练习里只有 5 个需要 Windows 变体，其余原样可用。因此孪生工程采用
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
| `13_character_io/02_eof_ferror` | `CLINGS_CHECK_INT(feof(f), 1)` | Microsoft CRT 的 `feof` 返回内部标志（`0x10`），不是 1 | 断言改为 `feof(f) != 0` |
| `17_translation_units/05_dynamic_linking` | `dlopen` / `dlsym` / `dlclose` | POSIX 动态加载，Windows 没有 `dlfcn.h` | `LoadLibraryA` / `GetProcAddress` / `FreeLibrary`，库名换成 `msvcrt.dll` |
| `19_modern_c_library/01_noreturn` | `fork` / `waitpid` | Windows 没有 `fork` | 子进程改为「用 `child` 参数重新执行自己」+ `_spawnv` / `_cwait` |

覆盖实现在 [`tools/windows_overrides.py`](../tools/windows_overrides.py)。替换要么
精确命中一次，要么直接报错，所以上游一改动这里就会失败而不是悄悄生成错误代码。

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
- `clings.cmd` 无法在 Wine 下验证：Wine 的 `cmd.exe` 需要真正的控制台，在无终端
  的环境里静默不执行。因此该脚本由 `real-windows` job 里的
  `cmd /c clings.cmd doctor` 以及人工冒烟清单覆盖。
- Wine 回路里 `wine` 每次冷启动约 4 秒，脚本用「预热 + 后台保活」把整轮压到
  一分钟以内；如果保活被环境杀掉，回路仍然正确，只是慢。
