# clings-win

`clings-win` 是 [clings](../cling) 的 Windows 孪生工程：同一套 185 个 C 练习，
Windows 原生入口、Windows 工具链、Windows 分发包，面向只有 Windows 的初学者。

它不是 fork，而是**生成物**。练习内容、参考答案、模板、测试框架、运行器全部
从上游仓库同步而来，唯一的差异记录在
[`tools/windows_overrides.py`](tools/windows_overrides.py) 里（6 个练习需要平台变体）。
因此两个工程不会各自漂移。

## 学习者怎么用

下载分发包（`dist/clings-win-<commit>.zip`），解压到一个**路径不含空格和中文**
的目录（例如 `D:\clings`），双击 `clings.cmd`：

```bat
clings.cmd list                 :: 列出全部练习
clings.cmd run                  :: 编译并运行下一个未完成练习
clings.cmd run 01_printf        :: 运行指定练习
clings.cmd hint 01_printf       :: 看提示
clings.cmd solution 01_printf   :: 看参考答案
clings.cmd reset 01_printf      :: 恢复初始文件
clings.cmd verify               :: 校验全部参考答案
clings.cmd doctor               :: 打印工具链信息
```

分发包自带编译器（w64devkit）和 Python，不需要安装、不需要管理员权限、
不需要改 PATH。如果拿到的是不含 `runtime\` 的精简包，则需要自己装
Python 3 和 MinGW-w64 GCC。

## 维护者怎么用

```sh
make sync            # 从 ../cling 同步练习并应用 Windows 覆盖
make check           # 检查孪生工程是否与上游一致（CI 用）
make winbox          # 在 .winbox/ 里准备 mingw-w64 + Wine（不需要 root）
make windows-check   # 交叉编译 + Wine 运行全部练习（Linux 上的 Windows 回路）
make winbox-native   # 额外拉取 w64devkit 和 Windows Python，用于打包
make package         # 产出 dist/clings-win-<commit>.zip
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
├── clings              # 运行器：上游版本 + 3 处 Windows 适配（生成物）
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
│   ├── windows_overrides.py # 唯一手写的平台差异
│   ├── winbox.sh            # 免 root 的 mingw-w64 + Wine 工具箱
│   ├── windows-check.sh     # 交叉编译 + Wine 全量回归
│   └── package_windows.py   # 打学习者分发包
└── Makefile
```

## 与上游的关系

- 练习内容的唯一事实来源是上游 `tools/specs_*.py` 和生成物。
- 本仓库**不直接编辑** `exercises/`、`solutions/`、`templates/`、`include/`，
  这几个目录每次 `make sync` 都会被覆盖。
- 要新增或修改练习：先改上游，再回到本仓库 `make sync`。
- `make check` 会在 CI 中验证本仓库等于「上游 commit + Windows 覆盖」。

## 许可

与上游一致，MIT License，见 [LICENSE](LICENSE)。
