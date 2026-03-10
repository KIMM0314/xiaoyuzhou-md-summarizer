@echo off
setlocal enabledelayedexpansion

set HERE=%~dp0
for %%I in ("%HERE%..\..\..") do set APP_DIR=%%~fI

set PYTHONPYCACHEPREFIX=%HERE%pycache
if not exist "%PYTHONPYCACHEPREFIX%" mkdir "%PYTHONPYCACHEPREFIX%"
python -m py_compile "%APP_DIR%\main.py"
if errorlevel 1 exit /b 1

findstr /n /c:"del model_obj" "%APP_DIR%\main.py" >nul
if errorlevel 1 exit /b 1

findstr /n /c:"gc.collect()" "%APP_DIR%\main.py" >nul
if errorlevel 1 exit /b 1

findstr /n /c:"def _transcribe_with_python_whisper" "%APP_DIR%\main.py" >nul
if errorlevel 1 exit /b 1

echo OK
exit /b 0
