# Validation bundle: RUN #19 (Task 3.1 / Ref R18)

## Scope
- Change ID: add-xiaoyuzhou-md-summarizer
- Task: 3.1 Fix file handle leak in `_read_text_file` [#R18]
- Validation scope: CLI

## How to run

### macOS / Linux
- From this folder, run: `bash run.sh`

### Windows
- From this folder, run: `run.bat`

## Pass / fail criteria

This bundle passes if all commands succeed:
- `python3 -m py_compile main.py` exits with code 0
- `grep -n "with open" main.py | grep "_read_text_file"` prints at least one matching line

