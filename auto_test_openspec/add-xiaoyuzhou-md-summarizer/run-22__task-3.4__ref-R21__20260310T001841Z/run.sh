#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
APP_DIR="$(cd "$HERE/../../.." && pwd)"

mkdir -p "$HERE/.pycache"
PYTHONPYCACHEPREFIX="$HERE/.pycache" python3 -m py_compile "$APP_DIR/main.py"

rg -n "def _transcribe_with_python_whisper" "$APP_DIR/main.py" >/dev/null
rg -n "shutil\.rmtree\(segment_dir, ignore_errors=True\)" "$APP_DIR/main.py" >/dev/null

APP_DIR="$APP_DIR" python3 - <<'PY'
import os
from pathlib import Path

app_dir = Path(os.environ["APP_DIR"])
text = (app_dir / "main.py").read_text(encoding="utf-8")
start = text.find("def _transcribe_with_python_whisper(")
if start < 0:
    raise SystemExit("missing _transcribe_with_python_whisper")
end = text.find("\ndef _run_whisper(", start)
snippet = text[start:end if end > start else None]
if "try:" not in snippet or "finally:" not in snippet:
    raise SystemExit("expected try/finally in _transcribe_with_python_whisper")
if "shutil.rmtree(segment_dir, ignore_errors=True)" not in snippet:
    raise SystemExit("expected guaranteed segment_dir cleanup call")
print("OK")
PY
