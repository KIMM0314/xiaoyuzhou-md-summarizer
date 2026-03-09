#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT_DIR"

export PYTHONPYCACHEPREFIX="${ROOT_DIR}/.pycache"
mkdir -p "$PYTHONPYCACHEPREFIX"
python3 -m py_compile main.py
grep -n "with open" main.py | grep "_read_text_file"
