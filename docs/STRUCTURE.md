## **📁 Estructura del Proyecto (Filesystem)**

```bash
mechbot-2x/
├── ai_core/
│   ├── dependency_analyzer.py       # Lógica principal de análisis de dependencias
│   ├── error_diagnosis_engine.py    # Motor de diagnóstico de errores
│   ├── auto_fix_module.py           # Módulo de autocorrección
│   └── knowledge_base/
│       ├── version_compatibility.db # Base de datos de compatibilidad
│       └── common_errors.json       # Errores frecuentes y soluciones
├── config/
│   ├── env_vars.yaml                # Variables de entorno
│   └── execution_profiles.yaml      # Perfiles de ejecución (dev, prod, testing)
├── logs/
│   ├── dependency_errors/           # Logs de fallos en dependencias
│   └── execution_traces/            # Trazas de ejecución de la IA
├── tests/
│   ├── integration_tests/           # Pruebas de integración
│   └── unit_tests/                  # Pruebas unitarias
├── scripts/
│   ├── setup_environment.sh         # Script de configuración inicial
│   └── auto_deploy.py               # Despliegue automático en CI/CD
└── README.md                        # Documentación del proyecto
```
