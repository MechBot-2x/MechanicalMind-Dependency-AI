# CONTRIBUTING.md para MechanicalMind Dependency AI

```markdown
# 🤖🚀 Guía de Contribución Galáctica 
# (MechMind Dependency AI v3.0)

Bienvenido/a al equipo de desarrollo interplanetario de MechanicalMind! Este documento explica cómo contribuir a nuestro sistema de gestión de dependencias con IA.

## 🌌 Primeros Pasos Cósmicos

1. **Configuración del Entorno**:
   ```bash
   # Clona el repositorio con todos los submódulos
   git clone --recurse-submodules https://github.com/MechBot-2x/MechanicalMind-Dependency-AI.git
   
   # Instala dependencias
   pip install -r requirements/dev.txt
   npm install
   ```

2. **Estructura del Proyecto**:
   ```
   /src                # Código fuente principal
     /ai_core         # Núcleo de IA
     /cli             # Interfaz de línea de comandos
   /docs              # Documentación
   /tests             # Pruebas automatizadas
   ```

## 🛠️ Flujo de Trabajo Cuántico

1. Crea una rama desde `main`:
   ```bash
   git checkout -b feature/nombre-de-tu-feature
   ```

2. Desarrolla tus cambios con tests:
   ```python
   # Ejemplo de test requerido
   def test_feature():
       assert amazing_feature() == expected_result
   ```

3. Genera diagramas actualizados:
   ```bash
   npm run build:diagrams
   ```

4. Ejecuta verificaciones pre-commit:
   ```bash
   pre-commit run --all-files
   ```

## ⚡ Protocolos de Código

- **Estilo de Código**: 
  ```bash
  black .  # Formateo automático
  flake8   # Verificación de estilo
  ```

- **Documentación**:
  - Docstrings en formato Google Style
  - Actualizar `docs/ARCHITECTURE.md` para cambios estructurales

## 🚀 Envío de Contribuciones

1. Crea un Pull Request a `main`
2. Asigna revisores del equipo
3. Espera que pasen los CI checks:
   - ✅ Tests unitarios
   - ✅ Verificación de dependencias
   - ✅ Generación de diagramas

## 🛰️ Self-Hosted Runners

Para ejecutores locales (requiere Docker):
```bash
# Configura el runner
docker-compose -f docker/runner.yml up -d

# Verifica estado
gh runner status
```

## 🆘 Soporte Técnico

¿Problemas con tu contribución? Contacta a:
- @mentores-ia (Slack)
- ia.mechmind@gmail.com (Email)

## 📜 Código de Conducta

Todos los contribuyentes deben seguir nuestro [Código Galáctico de Conducta](CODE_OF_CONDUCT.md).

¡Gracias por ayudar a construir el futuro de la gestión de dependencias! 🚀🤖💙
