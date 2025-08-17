#!/bin/bash
set -eo pipefail

export PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
export PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

DIAGRAM_DIR="docs/architecture/diagrams"
ERRORS=0

cd "$DIAGRAM_DIR"
for f in *.mmd; do
    echo "Generando ${f%.*}.png..."
    if npx mmdc \
        -i "$f" \
        -o "${f%.*}.png" \
        --backgroundColor transparent \
        --quiet \
        --puppeteerConfig '{"executablePath":"/usr/bin/chromium"}'; then
        echo "✓ Diagrama generado"
    else
        echo "✗ Error al generar el diagrama"
        ((ERRORS++))
    fi
done

if [ "$ERRORS" -gt 0 ]; then
    echo "⚠ Se encontraron $ERRORS errores"
    exit 1
else
    echo "✅ Todos los diagramas generados exitosamente"
fi
