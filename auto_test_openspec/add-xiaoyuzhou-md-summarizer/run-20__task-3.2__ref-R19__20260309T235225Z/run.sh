#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

mkdir -p /tmp/pycache
PYTHONPYCACHEPREFIX=/tmp/pycache python3 -m py_compile "${APP_DIR}/main.py"
grep -n "total_timeout" "${APP_DIR}/main.py"

