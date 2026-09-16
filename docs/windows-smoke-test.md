# 真机冒烟清单

自动化覆盖不了「小白第一次打开会怎样」。每次发布前，找一台干净的 Windows 10/11
机器（或虚拟机）按下面的顺序走一遍，任何一步不符合预期都算阻塞问题。

## 准备

- [ ] 使用一个**普通用户**账户，不要管理员权限。
- [ ] 把分发包解压到一个路径含中文和空格的目录，例如
      `C:\Users\测试 用户\桌面\clings win\`。
- [ ] 不要提前安装 Python、GCC、Visual Studio 或任何开发工具。

## 流程

1. [ ] 双击 `clings.cmd`：出现中文界面、列出 185 个练习，并且**没有**弹窗
       要求安装 Python。
2. [ ] 首次运行时 Windows Defender / SmartScreen **没有**拦截或误报。
3. [ ] 运行 `clings.cmd doctor`：编译器显示为随包自带的 gcc，路径正确。
4. [ ] 运行 `clings.cmd run 00_basics/01_printf`：故意失败，并显示**编译或测试
       诊断**（这是教学内容，不能是崩溃或乱码）。
5. [ ] 运行 `clings.cmd doctor`：`颜色:` 一行是 `开启`，并且 `clings.cmd list`
       的输出**真的是彩色**。Windows 10/11 的控制台都支持 ANSI，所以这一条
       不是"彩色或纯文本都可以"：退化成纯文本说明 VT 位没打开，按阻塞问题处理。
6. [ ] 上面两步的输出里**看不到** `[36m`、`[0m` 这类转义码——彩色文字里不该
       出现转义码，纯文本里也不该（见 [portability.md](portability.md)）。
7. [ ] 换终端再跑一次步骤 4 和 5：Windows Terminal（含 PowerShell 7）和传统
       conhost（cmd、Windows PowerShell 5.1）都必须是彩色，且都不出现转义码。
8. [ ] 用 VS Code 或记事本编辑该练习文件并保存，再跑一次 `run`：诊断随之变化。
9. [ ] 运行 `clings.cmd solution 00_basics/01_printf --apply` 后再 `run`：通过。
10. [ ] 运行 `clings.cmd reset 00_basics/01_printf`：文件回到初始状态，进度清除。
11. [ ] 运行 `clings.cmd run 18_advanced_c/03_pthreads`（先应用答案）：线程类练习
       能正常编译运行（验证 `libwinpthread-1.dll` 的部署）。
12. [ ] 运行 `clings.cmd watch 00_basics/01_printf`，保存文件后自动重跑，
       `Ctrl-C` 能正常退出。
13. [ ] 控制台中文不乱码；`Ctrl-C`、方向键、复制粘贴不产生异常输出。
14. [ ] 断网重试步骤 2 和 4：不应该因为缺少网络而失败。

## 记录

把结果（Windows 版本、步骤、截图、是否通过）附在发布 PR 里。若失败，请标明是
工具链问题、路径/权限问题，还是教学内容问题——这三类要走不同的修复路径。
