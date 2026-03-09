@echo off
setlocal enabledelayedexpansion

REM Jump to repo root (app/)
cd /d %~dp0\..\..\..

set PYTHONPYCACHEPREFIX=%CD%\.pycache
if not exist "%PYTHONPYCACHEPREFIX%" mkdir "%PYTHONPYCACHEPREFIX%"
python3 -m py_compile main.py
if errorlevel 1 exit /b 1

where grep >nul 2>nul
if %errorlevel%==0 (
  grep -n "with open" main.py | grep "_read_text_file"
  if errorlevel 1 exit /b 1
) else (
  findstr /n /c:"with open" main.py | findstr /c:"_read_text_file"
  if errorlevel 1 exit /b 1
)

endlocal
