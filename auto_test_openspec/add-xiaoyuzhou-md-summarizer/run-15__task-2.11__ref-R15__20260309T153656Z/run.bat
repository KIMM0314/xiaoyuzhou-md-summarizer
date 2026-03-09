@echo off
setlocal
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%\..\..\.."
python3 -m py_compile main.py && rg -n "segment_seconds = 600" main.py
