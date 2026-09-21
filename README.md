# clings-win

`clings-win` 是 [clings](https://github.com/WindDevil/clings) 的 Windows 版：
184 道 C 练习，换成 Windows 的入口、工具链和分发包，给只用 Windows 的
初学者。题目的标题、学习目标、提示、注释和命令行输出都是中文，代码里的标识符、
函数名和格式说明符保持英文，方便对着教材和报错查。分发包自带编译器和 Python，
解压后双击 `clings.cmd` 就能开始。

练习内容、参考答案、模板、测试框架和运行器都从上游同步过来，本仓库只保存差异，
一共四处：
[`tools/windows_overrides.py`](tools/windows_overrides.py)（12 个练习需要平台变体）、
[`tools/sync_from_source.py`](tools/sync_from_source.py) 里的 `RUNNER_PATCHES`
（运行器的 Windows 适配，以及跑失败之后给新手的那三行提示）、
[`tools/zh_glossary.py`](tools/zh_glossary.py)
加 [`tools/zh_translate.py`](tools/zh_translate.py)（中英对照表，另有
`./clings` 这类 POSIX 命令行的 Windows 改写），以及
[`tools/curriculum.py`](tools/curriculum.py)（课程序列：主题的教学顺序、不再重复
的练习、补上的中间难度练习）。`make check` 在 CI 里核对「上游 + 这四处差异」
的结果，两边不会各写一份。

## 学习者怎么用

发布页有两个包：

| 包 | 大小 | 适合谁 |
| --- | ---: | --- |
| `clings-win-<commit>-full.zip` | 约 190 MB | 机器上没装任何开发工具的人。自带编译器（w64devkit）和 Python |
| `clings-win-<commit>-slim.zip` | 约 0.6 MB | 已经装了 Python 3 和 MinGW-w64 GCC 的人 |

`<commit>` 是本仓库的 commit，所以每次重建出来的文件名都不同；上游 commit 记在
[`docs/provenance.md`](docs/provenance.md)。

解压到哪个目录都可以，双击 `clings.cmd`。第一次运行会先把用法讲一遍，再编译并
测试第一道题，跑完停在这个菜单上：

```text
── 第一次用，先看这里 ─────────────────────────────────────
  这个包里有 184 道 C 语言练习题，每道题都是一个能编译、能运行的程序，
  里面留了一处空（注释里写着 TODO）。打开文件、把空补上、保存，再跑一遍就会通过。

  一开始不通过是正常的：报错就是这道题给你的线索，不是环境装坏了。
  做过的题会记下来，下次双击 clings.cmd 接着做没做完的那一道。

  改文件有三种办法，挑一种就行：
    记事本      在 exercises\ 里找到练习文件，右键 →「打开方式」→ 记事本
    VS Code     跑完在下面的菜单里按 2
    内置编辑器   在下面的菜单里按 3，用浏览器写，有高亮和自动查错

── 00_basics/01_printf  用 printf 打印 ──────────────
  用 printf 打印一行文本。
  要改的文件: exercises\00_basics\01_printf.c

运行 00_basics/01_printf - 用 printf 打印
  未通过
  FAIL D:\clings\exercises\00_basics\01_printf.c:20: print_greeting() == 10 (got 14, want 10)

1 of 1 checks failed.
Hello, world!

  这道题一开始就是通不过的：文件里留了空（注释里的 TODO），报错就是它给的线索。
  要改的文件:  exercises\00_basics\01_printf.c
  看提示:      .\clings.cmd hint 00_basics/01_printf
  改完重跑:    .\clings.cmd run 00_basics/01_printf

1 个练习未通过

  [1] 改完了，重跑一遍
  [2] 用 VS Code 打开 exercises\00_basics\01_printf.c
  [3] 打开内置编辑器（浏览器）
  [4] 看这道题的提示
  [0] 退出

选择:
```

「第一次用，先看这里」那段只在还没通过任何一道题时出现。之后每次双击都一样：
跑当前这道题，然后给菜单。菜单里 `1` 是重跑，`2` 用 VS Code 打开菜单里列出的
那个文件，`3` 用浏览器里的内置编辑器打开，`4` 看这道题的提示。做过的题记在
`.clings\progress.json` 里，下次双击接着做没做完的那一道。

每道题发到手上时都是坏的：留了一处空，编译器或测试框架报的错就是题目本身，
所以第一次跑必然不通过。改文件，按 `1` 重跑，通过之后它会告诉你下一道题在哪。

命令行的完整用法：

| 命令 | 作用 |
| --- | --- |
| `.\clings.cmd` | 双击就是这个：编译并测试当前练习，然后停在菜单 |
| `.\clings.cmd list` | 列出全部练习和完成情况 |
| `.\clings.cmd run` | 编译并运行下一个未完成的练习 |
| `.\clings.cmd run 00_basics/01_printf` | 运行指定练习，不通过时打印下一步做什么 |
| `.\clings.cmd hint 00_basics/01_printf` | 看这道题的提示 |
| `.\clings.cmd solution 00_basics/01_printf` | 看参考答案 |
| `.\clings.cmd reset 00_basics/01_printf` | 把练习文件恢复成初始状态 |
| `.\clings.cmd verify` | 校验全部参考答案 |
| `.\clings.cmd doctor` | 打印 Python、编译器、编译参数和颜色判断 |
| `.\clings.cmd open 00_basics/01_printf` | 用 VS Code 打开这道练习 |
| `.\clings.cmd web` | 打开内置的网页编辑器 |

练习名写全 `主题/文件名` 最省事。只写 `01_printf` 这种短名时，如果不止一道题匹配
（`00_basics/01_printf` 和 `12_standard_library/01_printf_formats` 都能匹配上），
clings 会把候选列出来然后停下，不会替你挑一道。

开头的 `.\` 是给 PowerShell 看的：它不在当前目录里找命令，写 `clings.cmd` 会报
「无法识别」。cmd.exe 两种写法都认，`.\clings.cmd` 两边都能用。

路径里有中文或空格也要能跑，发布前的验收清单就是拿
`C:\Users\测试 用户\桌面\clings win\` 试的。真遇到和路径有关的怪问题，先换到
纯英文、无空格的目录再试一次，然后在仓库的 Issues 里说一声。

`-full.zip` 不用安装任何东西，不需要管理员权限，也不用改 PATH。`-slim.zip` 里没有
`runtime\`，要自己装 Python 3 和 MinGW-w64 GCC；装了但没进 PATH 时，`run` 会
打印一条中文说明告诉你去哪找，并让你用 `doctor` 看当前工具链。

## 怎么改练习文件

练习就是普通的 `.c` 文件，三条路挑一条：

| 方式 | 怎么进 | 需要什么 |
| --- | --- | --- |
| 记事本 | 在 `exercises\` 里找到练习文件，右键「打开方式」→ 记事本 | 什么也不用装 |
| VS Code | 菜单里按 `2`，或 `.\clings.cmd open 00_basics/01_printf` | 自己装 VS Code 和 C/C++ 扩展 |
| 内置编辑器 | 菜单里按 `3`，或 `.\clings.cmd web` | 什么也不用装，用浏览器 |

用 VS Code 打开的是**整个包目录**，包里带的 `.vscode/c_cpp_properties.json`
已经把 `include/` 配好，所以补全、跳转和 `CLINGS_CHECK` 这些宏都认得。

内置编辑器在浏览器里打开，可以：

- 左侧按主题列出全部练习，标出做完的进度；
- 代码高亮（C 的语法、括号匹配、折叠）；
- **边写边查语法**：用的是 `run` 编译这道题时的同一套编译参数，所以两边报的错
  一致，错误会同时出现在行号的标记和下方的问题列表里；
- **代码提示**：`Ctrl-Space` 手动呼出，输入两个字以后自动弹出；提示来自 C 标准库
  （带函数签名和所属头文件）、关键字、常用代码片段，以及**这个练习自己声明的
  名字**；
- `Ctrl-S` 保存、`Ctrl-Enter` 运行，另有参考答案、应用、重置、看提示的按钮。

它只监听 `127.0.0.1`，页面带一次性令牌，别的网页打不开、也调不动接口；文件读写
限定在运行器列出的这道题的文件里。`studio\` 目录是可选的：删掉之后练习照样编译、
运行、检查，只是没有内置编辑器，这时双击 `clings.cmd` 会说明这一点，然后直接
编译运行下一道题。

命令行的颜色跟着终端走：Windows Terminal 和现代控制台上是彩色，遇到不认识 ANSI
的老式控制台就退回纯文本，不会打出 `[36m` 这类转义码。想手动控制，就在同一个
窗口里先设环境变量再运行：cmd 用 `set CLINGS_COLOR=always`，PowerShell 用
`$env:CLINGS_COLOR="always"`；`never` 关掉颜色，通用的 `NO_COLOR` 也认。
`clings.cmd doctor` 会打印当前的判断和原因。

## 维护者怎么用

```sh
make sync            # 从 ../cling 同步练习并应用 Windows 覆盖
make check           # 检查孪生工程是否与上游一致（CI 用）
make test            # 跑 studio 和打包的测试（没编译器时跳过需要编译的那部分）
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
里的 `real-windows` job 提供（GitHub 的 `windows-latest` runner），它还会解开
刚打好的分发包、用包里自带的 Python 跑一遍 `clings.cmd`——打包出错的地方，
单测是看不出来的，见 [`docs/portability.md`](docs/portability.md#自带的-python)
里那条 `._pth` 的坑；发布前的人工验收按
[`docs/windows-smoke-test.md`](docs/windows-smoke-test.md) 走一遍。

## 目录结构

```text
clings-win/
├── clings              # 运行器：上游版本 + Windows 适配（生成物）
├── clings.cmd          # Windows 双击入口：找 Python、加 PATH，转交 CLI 或 studio
├── .vscode/            # 手写：让 VS Code 的 C/C++ 扩展找到 include/
├── exercises/          # 生成物：初始练习
├── solutions/          # 生成物：参考答案
├── templates/          # 生成物：reset 用的原始练习
├── include/clings/     # 生成物：自带测试框架
├── studio/             # 手写：双击菜单、VS Code 入口、内置网页编辑器（可删）
│   ├── bridge.py       #   └ 唯一和运行器说话的地方：跑它，读它的 --json
│   ├── menu.py         #     双击后的流程：入门说明、跑题、菜单
│   ├── vscode.py       #     找 VS Code，用「一个窗口 + 整个包目录」打开
│   ├── server.py       #     内置编辑器的后端（stdlib，只监听 127.0.0.1）
│   ├── languages/      #     语言插件：c.py 问编译器，plain.py 什么也不答
│   ├── web/            #     前端：无构建步骤，vendor/ 里是 CodeMirror 5 和 marked
│   └── tests/          #     测试（不打进分发包）
├── docs/
│   ├── provenance.md   # 生成物：上游仓库、commit、练习数量
│   ├── portability.md  # 可移植性评估与 Windows 覆盖说明
│   └── windows-smoke-test.md  # 真机人工验收清单
├── tools/
│   ├── sync_from_source.py  # 从上游生成孪生工程
│   ├── windows_overrides.py # 手写的平台差异：12 个练习的 Windows 变体
│   ├── winbox.sh            # 免 root 的 mingw-w64 + Wine 工具箱
│   ├── windows-check.sh     # 交叉编译 + Wine 全量回归
│   ├── package_windows.py   # 打学习者分发包
│   └── tests/               # 打包与运行器提示的测试（不打进分发包）
└── Makefile
```

## 与上游的关系

- 练习内容的唯一事实来源是上游 `tools/specs_*.py` 和生成物。
- 本仓库**不直接编辑** `exercises/`、`solutions/`、`templates/`、`include/`，
  这几个目录每次 `make sync` 都会被覆盖。
- 要新增或修改练习：先改上游，再回到本仓库 `make sync`。如果新练习带来新的
  英文标题、提示或注释，`make sync` 会直接报错并列出缺哪几条，把
  [`tools/zh_glossary.py`](tools/zh_glossary.py) 补齐即可。
- `make check` 在 CI 里验证本仓库等于「上游 + 上面那三处差异」。

## 许可

与上游一致，MIT License，见 [LICENSE](LICENSE)。
