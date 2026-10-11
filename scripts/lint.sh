#!/usr/bin/env bash
# Lint + format + test en una pasada. Uso: bash scripts/lint.sh
set -e
cd "$(dirname "$0")/.."
source ~/mechmind-env/bin/activate

echo "── 1/3 Ruff check (solo src/) ──"
ruff check src --fix || true
ruff check src

echo
echo "── 2/3 Black (solo src/) ──"
black src

echo
echo "── 3/3 Tests ──"
python -m pytest

echo
echo "✅ Todo OK"
