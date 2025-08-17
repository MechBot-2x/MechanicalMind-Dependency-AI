#!/bin/bash

set -eo pipefail

# Paso 1: Instalar dependencias
sudo apt-get update
sudo apt-get install -y docker.io npm python3-venv

# Paso 2: Configurar entorno
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# Paso 3: Generar documentación
./scripts/integrate_docs.sh

# Paso 4: Validar
pre-commit run --all-files
pytest tests/documentation_test.py

# Paso 5: Commit seguro
if git status --porcelain | grep -q "M"; then
  git add .
  git commit -m "Integración automática de documentación $(date +%Y%m%d)"
  git push
fi
