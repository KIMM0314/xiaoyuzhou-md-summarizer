#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$APP_ROOT"
python3 main.py summarize --help | grep -F "default: 120"
