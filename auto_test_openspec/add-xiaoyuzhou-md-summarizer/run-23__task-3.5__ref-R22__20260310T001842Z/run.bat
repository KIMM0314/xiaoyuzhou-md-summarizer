@echo off
setlocal enabledelayedexpansion

set HERE=%~dp0
for %%I in ("%HERE%..\..\..") do set APP_DIR=%%~fI

python -m py_compile "%APP_DIR%\main.py"
if errorlevel 1 exit /b 1

findstr /n /c:"def _extract_http_status_code" "%APP_DIR%\main.py" >nul
if errorlevel 1 exit /b 1

findstr /n /c:"400 <= status_code < 500" "%APP_DIR%\main.py" >nul
if errorlevel 1 exit /b 1

echo OK
exit /b 0
