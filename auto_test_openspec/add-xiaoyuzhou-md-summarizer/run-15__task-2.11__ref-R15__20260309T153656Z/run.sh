#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$APP_ROOT"
python3 -m py_compile main.py && rg -n "segment_seconds = 600" main.py
