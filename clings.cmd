@echo off
rem clings for Windows - double-click friendly entry point.
rem
rem Finds a Python interpreter (preferring the bundled one), puts the bundled
rem mingw-w64 compiler on PATH and hands over to the clings runner.
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

if "%~1"=="" (
  echo [clings] Tip: run "clings.cmd run" to compile and test the next exercise.
  %PY% "%ROOT%clings" list
) else (
  %PY% "%ROOT%clings" %*
)
exit /b %ERRORLEVEL%
