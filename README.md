# clings-win

`clings-win` 是 [clings](../cling) 的 Windows 孪生工程：同一套 185 个 C 练习，
Windows 原生入口、Windows 工具链、Windows 分发包，面向只有 Windows 的初学者。
练习的标题、学习目标、提示、注释和命令行输出都是中文，代码本身（标识符、
函数名、格式说明符）保持英文，和标准教材、报错信息对得上。

它不是 fork，而是**生成物**。练习内容、参考答案、模板、测试框架、运行器全部
从上游仓库同步而来，差异只记录在三处：
[`tools/windows_overrides.py`](tools/windows_overrides.py)（12 个练习需要平台变体）、
[`tools/sync_from_source.py`](tools/sync_from_source.py) 里的 `RUNNER_PATCHES`
（运行器的 Windows 适配）和 [`tools/zh_glossary.py`](tools/zh_glossary.py)
加 [`tools/zh_translate.py`](tools/zh_translate.py)（中英对照表，另有
`./clings` 这类 POSIX 命令行的 Windows 改写）。因此两个工程不会各自漂移。

## 学习者怎么用

发布页提供两个包，按自己的情况挑一个：

| 包 | 大小 | 适合谁 |
| --- | ---: | --- |
| `clings-win-<commit>-full.zip` | 约 190 MB | 机器上什么都没有的人。自带编译器（w64devkit）和 Python，解压就能用 |
| `clings-win-<commit>-slim.zip` | 约 0.4 MB | 已经装了 Python 3 和 MinGW-w64 GCC 的人 |

`<commit>` 是本仓库的 commit（上游 commit 见 `docs/provenance.md`），所以每次重建
文件名都不同，不会和上一版混淆。

解压到一个**路径不含空格和中文**的目录（例如 `D:\clings`），双击 `clings.cmd`：

```bat
.\clings.cmd list                 :: 列出全部练习
.\clings.cmd run                  :: 编译并运行下一个未完成练习
.\clings.cmd run 01_printf        :: 运行指定练习
.\clings.cmd hint 01_printf       :: 看提示
.\clings.cmd solution 01_printf   :: 看参考答案
.\clings.cmd reset 01_printf      :: 恢复初始文件
.\clings.cmd verify               :: 校验全部参考答案
.\clings.cmd doctor               :: 打印工具链信息
```

开头的 `.\` 是给 PowerShell 看的：它不会在当前目录里找命令，写 `clings.cmd`
会报"无法识别"。cmd.exe 两种写法都认，所以 `.\clings.cmd` 是两边都能用的一种。

分发包自带编译器（w64devkit）和 Python，不需要安装、不需要管理员权限、
不需要改 PATH。`-slim.zip` 不含 `runtime\`，需要自己准备 Python 3 和
MinGW-w64 GCC。

命令行颜色会自动适应当前的终端：Windows Terminal 和现代控制台上是彩色的，
在不认识 ANSI 的老式控制台上自动退回纯文本，不会打出 `[36m` 这类转义码。
想手动控制，就在同一个窗口里先设环境变量再运行——cmd 里用
`set CLINGS_COLOR=always`，PowerShell 里用 `$env:CLINGS_COLOR="always"`；
`never` 关掉颜色，通用的 `NO_COLOR` 也认。`clings.cmd doctor` 会打印它当前
的判断和原因。

## 维护者怎么用

```sh
make sync            # 从 ../cling 同步练习并应用 Windows 覆盖
make check           # 检查孪生工程是否与上游一致（CI 用）
make winbox          # 在 .winbox/ 里准备 mingw-w64 + Wine（不需要 root）
make windows-check   # 交叉编译 + Wine 运行全部练习（Linux 上的 Windows 回路）
make winbox-native   # 额外拉取 w64devkit 和 Windows Python，用于打包
make package         # 产出 dist/ 下的 slim 和 full 两个 zip
```

没有 Windows 机器时，`make windows-check` 就是日常回路：它用 mingw-w64 把每个
练习编成真正的 PE 可执行文件，再用 Wine 跑，并且复用孪生工程自己的 `clings`
运行器，所以 CLI 逻辑也一并被覆盖。实测结果见
[`docs/portability.md`](docs/portability.md)。

真机 ground truth 由 [`.github/workflows/windows.yml`](.github/workflows/windows.yml)
里的 `real-windows` job 提供（GitHub 的 `windows-latest` runner）；发布前的人工
验收按 [`docs/windows-smoke-test.md`](docs/windows-smoke-test.md) 走一遍。

## 目录结构

```text
clings-win/
├── clings              # 运行器：上游版本 + Windows 适配（生成物）
├── clings.cmd          # Windows 双击入口：找 Python、加 PATH、转交 CLI
├── exercises/          # 生成物：初始练习
├── solutions/          # 生成物：参考答案
├── templates/          # 生成物：reset 用的原始练习
├── include/clings/     # 生成物：自带测试框架
├── docs/
│   ├── provenance.md   # 生成物：上游仓库、commit、练习数量
│   ├── portability.md  # 可移植性评估与 Windows 覆盖说明
│   └── windows-smoke-test.md  # 真机人工验收清单
├── tools/
│   ├── sync_from_source.py  # 从上游生成孪生工程
│   ├── windows_overrides.py # 手写的平台差异：12 个练习的 Windows 变体
│   ├── winbox.sh            # 免 root 的 mingw-w64 + Wine 工具箱
│   ├── windows-check.sh     # 交叉编译 + Wine 全量回归
│   └── package_windows.py   # 打学习者分发包
└── Makefile
```

## 与上游的关系

- 练习内容的唯一事实来源是上游 `tools/specs_*.py` 和生成物。
- 本仓库**不直接编辑** `exercises/`、`solutions/`、`templates/`、`include/`，
  这几个目录每次 `make sync` 都会被覆盖。
- 要新增或修改练习：先改上游，再回到本仓库 `make sync`。如果新练习带来新的
  英文标题、提示或注释，`make sync` 会直接报错并列出缺哪几条，把
  [`tools/zh_glossary.py`](tools/zh_glossary.py) 补齐即可。
- `make check` 会在 CI 中验证本仓库等于「上游 commit + Windows 覆盖」。

## 许可

与上游一致，MIT License，见 [LICENSE](LICENSE)。
