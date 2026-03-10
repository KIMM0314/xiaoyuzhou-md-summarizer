#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
APP_DIR="$(cd "$HERE/../../.." && pwd)"

mkdir -p "$HERE/.pycache"
PYTHONPYCACHEPREFIX="$HERE/.pycache" python3 -m py_compile "$APP_DIR/main.py"

# Grep verification: explicit cleanup calls
rg -n "del model_obj" "$APP_DIR/main.py" >/dev/null
rg -n "gc\.collect\(\)" "$APP_DIR/main.py" >/dev/null

# Pattern check: ensure model usage is protected by try/finally in _transcribe_with_python_whisper
APP_DIR="$APP_DIR" python3 - <<'PY'
import os
from pathlib import Path

app_dir = Path(os.environ["APP_DIR"])
lines = (app_dir / "main.py").read_text(encoding="utf-8").splitlines(True)

start = None
for i, line in enumerate(lines):
    if line.startswith("def _transcribe_with_python_whisper("):
        start = i
        break
if start is None:
    raise SystemExit("Could not locate _transcribe_with_python_whisper")

end = None
for j in range(start + 1, len(lines)):
    if lines[j].startswith("def "):
        end = j
        break
snippet = "".join(lines[start : end if end is not None else len(lines)])

if "try:" not in snippet or "finally:" not in snippet:
    raise SystemExit("Expected try/finally in _transcribe_with_python_whisper")

if "del model_obj" not in snippet or "gc.collect()" not in snippet:
    raise SystemExit("Expected del model_obj and gc.collect() in _transcribe_with_python_whisper")
print("OK")
PY
