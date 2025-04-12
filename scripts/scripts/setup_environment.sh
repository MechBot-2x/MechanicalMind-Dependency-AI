#!/bin/bash

# Configuración inicial del entorno para MechanicalMind Dependency AI v2.0

echo "🚀 Iniciando configuración del entorno..."

# 1. Validar si Python está instalado
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 no está instalado. Por favor, instálalo para continuar."
    exit 1
fi
echo "✅ Python3 encontrado."

# 2. Crear un entorno virtual
if [ ! -d "venv" ]; then
    echo "📁 Creando entorno virtual..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado."
else
    echo "📁 Entorno virtual ya existe. Usando el existente."
fi

# Activar entorno virtual
echo "🔑 Activando entorno virtual..."
source venv/bin/activate

# 3. Instalar dependencias desde requirements.txt
if [ -f "requirements.txt" ]; then
    echo "📦 Instalando dependencias desde requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencias instaladas correctamente."
else
    echo "❌ No se encontró el archivo requirements.txt. Por favor, verifica."
    exit 1
fi

# 4. Configurar variables de entorno
if [ -f "config/env_vars.yaml" ]; then
    echo "🔧 Configurando variables de entorno desde config/env_vars.yaml..."
    export $(grep -v '^#' config/env_vars.yaml | xargs)
    echo "✅ Variables de entorno cargadas."
else
    echo "⚠️ Archivo config/env_vars.yaml no encontrado. Saltando configuración de variables de entorno."
fi

# 5. Mensaje final
echo "🎉 Configuración del entorno completada. ¡Listo para empezar!"