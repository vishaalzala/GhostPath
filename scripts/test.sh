#!/usr/bin/env bash
# Local v2 tests; no root privileges.
set -Eeuo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ ! -x .venv/bin/python ]]; then
  echo "Create a venv first: bash scripts/setup-dev.sh" >&2
  exit 1
fi
.venv/bin/python -m compileall -q src tests
.venv/bin/python -m unittest discover -s tests -v
