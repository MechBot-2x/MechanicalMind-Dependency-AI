#!/bin/bash

# Verificar sintaxis YAML/JSON
yamllint .github/workflows/
python -m json.tool docs/*.json > /dev/null

# Generar diagramas
npm run build:diagrams || {
  echo "Local diagram generation failed, trying Docker..."
  docker-compose -f docker-compose.mermaid.yml up --build
}

# Consolidar documentación
find docs/ -name "*.md" -type f -exec cat {} \; > docs/consolidated.md

# Validar estructura
if ! grep -q "MechanicalMind Dependency AI" docs/consolidated.md; then
  echo "Error: Document structure validation failed"
  exit 1
fi

echo "Documentation integration completed successfully"
