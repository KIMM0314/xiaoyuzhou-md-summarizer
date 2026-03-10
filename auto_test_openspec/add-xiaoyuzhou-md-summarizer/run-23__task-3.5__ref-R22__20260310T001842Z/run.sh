#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
APP_DIR="$(cd "$HERE/../../.." && pwd)"

mkdir -p "$HERE/.pycache"
PYTHONPYCACHEPREFIX="$HERE/.pycache" python3 -m py_compile "$APP_DIR/main.py"

rg -n "def _extract_http_status_code" "$APP_DIR/main.py" >/dev/null
rg -n "400 <= status_code < 500" "$APP_DIR/main.py" >/dev/null

APP_DIR="$APP_DIR" python3 - <<'PY'
import os
import sys

sys.path.insert(0, os.environ["APP_DIR"])
import main  # noqa: E402

calls_4xx = {"n": 0}

class Http404(Exception):
    code = 404

def action_4xx():
    calls_4xx["n"] += 1
    raise Http404("not found")

try:
    main._retry_with_backoff(
        "test-4xx",
        action_4xx,
        retries=3,
        backoff_seconds=(0, 0, 0),
        total_timeout=5,
    )
except RuntimeError:
    pass
else:
    raise SystemExit("expected RuntimeError for 4xx")

if calls_4xx["n"] != 1:
    raise SystemExit(f"expected 4xx attempts=1, got {calls_4xx['n']}")

calls_5xx = {"n": 0}

class Http503(Exception):
    code = 503

def action_5xx():
    calls_5xx["n"] += 1
    raise Http503("server busy")

try:
    main._retry_with_backoff(
        "test-5xx",
        action_5xx,
        retries=2,
        backoff_seconds=(0, 0),
        total_timeout=5,
    )
except RuntimeError:
    pass
else:
    raise SystemExit("expected RuntimeError for 5xx after retries")

if calls_5xx["n"] != 3:
    raise SystemExit(f"expected 5xx attempts=3, got {calls_5xx['n']}")

print("OK")
PY
