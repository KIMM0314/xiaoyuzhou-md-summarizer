@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "APP_DIR=%SCRIPT_DIR%..\..\.."

python -m py_compile "%APP_DIR%\\main.py"
if errorlevel 1 exit /b 1

findstr /n "total_timeout" "%APP_DIR%\\main.py"
exit /b %errorlevel%

