@echo off
setlocal
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%\..\..\.."
python3 -c "import main; print('OK')" && python3 main.py summarize --help | grep force
