@echo off
rem clings for Windows - double-click friendly entry point.
rem
rem Finds a Python interpreter (preferring the bundled one), puts the bundled
rem mingw-w64 compiler on PATH and hands over: to the studio for `open`, `web`,
rem `menu` and for a double-click with no arguments, and to the clings runner
rem for everything else.
rem
rem The studio (studio\) is optional.  Delete that directory and every exercise
rem still compiles, runs and checks; only the built-in editor goes away.
setlocal enableextensions
chcp 65001 >nul 2>&1
rem Python would otherwise encode its output with the console code page and
rem fail on Chinese text.
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

set "ROOT=%~dp0"
set "PATH=%ROOT%runtime\mingw\bin;%ROOT%runtime\python;%PATH%"
if not defined CC set "CC=gcc"

set "PY="
if exist "%ROOT%runtime\python\python.exe" set "PY=%ROOT%runtime\python\python.exe"

if not defined PY (
  py -3 -V >nul 2>&1
  if not errorlevel 1 set "PY=py -3"
)

if not defined PY (
  python -V >nul 2>&1
  if not errorlevel 1 set "PY=python"
)

if not defined PY (
  echo [clings] Python 3 was not found.
  echo [clings] Install it from https://www.python.org/downloads/windows/
  echo [clings] or use a package that bundles runtime\python.
  pause
  exit /b 1
)

rem Whether this console closes the moment we are done.  Explorer starts the
rem script as `cmd /c ""D:\...\clings.cmd" "`, and anything else that goes
rem through cmd - PowerShell, `start`, a shortcut - leaves the same kind of
rem command line, so the script name shows up in %cmdcmdline%.  An open cmd.exe
rem has only its own path there, and that window stays open by itself.
rem
rem So this rule cannot tell Explorer from PowerShell, and the two want
rem opposite things: Explorer's console vanishes unless we pause, PowerShell's
rem is still there and the pause is a wasted keypress.  We pause anyway.  The
rem two ways of being wrong are not symmetrical - one is a keypress, the other
rem is the window closing before the learner has read a single line.
set "INTERACTIVE="
echo %cmdcmdline% | find /i "%~nx0" >nul 2>&1
if not errorlevel 1 set "INTERACTIVE=1"

set "STUDIO="
if exist "%ROOT%studio\__main__.py" set "STUDIO=1"

if "%~1"=="" goto default
if /i "%~1"=="open" goto studio
if /i "%~1"=="web" goto studio
if /i "%~1"=="menu" goto studio

%PY% "%ROOT%clings" %*
exit /b %ERRORLEVEL%

:studio
if not defined STUDIO (
  echo [clings] 这个包里没有内置编辑器（studio\ 目录不存在）。
  echo [clings] 用 "%~nx0 run" 编译并测试，或者安装 VS Code 再用 "%~nx0 open"。
  if defined INTERACTIVE pause
  exit /b 1
)
set "PYTHONPATH=%ROOT%"
%PY% -m studio %*
set "CODE=%ERRORLEVEL%"
if defined INTERACTIVE pause
exit /b %CODE%

:default
rem No arguments: the first thing a learner sees should be the next exercise
rem being compiled and tested, not a bare list that scrolls away.
if not defined STUDIO (
  echo [clings] Tip: run "clings.cmd run" to compile and test the next exercise.
  %PY% "%ROOT%clings" run
  set "CODE=%ERRORLEVEL%"
  if defined INTERACTIVE pause
  exit /b %CODE%
)
set "PYTHONPATH=%ROOT%"
%PY% -m studio menu
set "CODE=%ERRORLEVEL%"
if defined INTERACTIVE pause
exit /b %CODE%
