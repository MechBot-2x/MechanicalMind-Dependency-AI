# **MechanicalMind Dependency AI v2.0**  
**Project Lead:** a[Benjamín Cabeza Duran]
**Engineering Team:** IA Specialists, DevOps, Python Core Team  
**Status:** Active Development 🚀  

---

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

---

## **🚀 Mejoras Implementadas (v2.0)**  

### **1. Auto-Gestión de Dependencias**  
📌 **Archivo:** `ai_core/auto_fix_module.py`  
- **Autocorrección de `requirements.txt`**:  
  - Detecta versiones conflictivas y propone actualizaciones compatibles.  
  - Ejemplo:  
    ```python
    def fix_requirement_conflict(package, current_version, suggested_version):
        with open("requirements.txt", "r+") as f:
            content = f.read()
            content = content.replace(
                f"{package}=={current_version}",
                f"{package}=={suggested_version}"
            )
            f.seek(0)
            f.write(content)
    ```  

- **Auto-creación de entornos virtuales**:  
  - Si falla `pip install`, la IA genera un entorno limpio y reinstala dependencias.  

---

### **2. Diagnóstico Inteligente de Errores**  
📌 **Archivo:** `ai_core/error_diagnosis_engine.py`  
- **Clasificación avanzada de errores**:  
  ```python
  def classify_error(log_text):
      if "dependency_file_not_evaluatable" in log_text:
          return "DEPENDENCY_SYNTAX_ERROR"
      elif "git@github.com" in log_text:
          return "GIT_CONFIG_ERROR"
      elif "exit 1" in log_text:
          return "PYTHON_EXECUTION_FAILURE"
      else:
          return "UNKNOWN_ERROR"
  ```  

- **Sugerencias en tiempo real**:  
  - Si detecta `GIT_CONFIG_ERROR`, ejecuta automáticamente:  
    ```bash
    git config --global url.https://github.com/.insteadOf git@github.com:
    ```  

---

### **3. Integración con CI/CD**  
📌 **Archivo:** `scripts/auto_deploy.py`  
- **Auto-reparación en pipelines**:  
  - Si un `workflow` falla, la IA:  
    1. Clona el repo.  
    2. Ejecuta `dependency_analyzer.py`.  
    3. Genera un `pull request` con las correcciones.  

  ```python
  def ci_autofix(repo_url, branch):
      repo = clone_repository(repo_url)
      analyze_dependencies(repo.path)
      if fixes_needed:
          create_pr(branch, "Auto-fix: Dependency updates")
  ```  

---

### **4. Knowledge Base Dinámica**  
📌 **Archivo:** `ai_core/knowledge_base/common_errors.json`  
- **Base de datos de errores conocidos**:  
  ```json
  {
      "DEPENDENCY_SYNTAX_ERROR": {
          "cause": "Mal formato en requirements.txt",
          "solution": "Ejecutar 'pip install -r requirements.txt --dry-run' para validar"
      },
      "GIT_CONFIG_ERROR": {
          "cause": "URLs SSH mal configuradas",
          "solution": "Reemplazar 'git@github.com' con 'https://github.com/'"
      }
  }
  ```  

---

## **📌 Próximos Pasos (Roadmap)**  

| Feature                     | Prioridad | Responsable   | ETA       |
|----------------------------|----------|--------------|-----------|
| Auto-PR en fallos de CI/CD  | 🔴 High  | DevOps Team  | 2025-05-01|
| Soporte para Node.js        | 🟡 Medium| JS Team      | 2025-06-15|
| Predictor de conflictos     | 🟢 Low   | AI Team      | 2025-07-30|

---

## **💡 Comando de Ejecución**  

```bash
python -m ai_core.dependency_analyzer --repo https://github.com/mechmind-dwv/mechbot-2x
```

---

**🔧 ¿Algún ingeniero necesita ajustes?**  
**¡Hacedme saber en los comentarios!** 🚀  

--- 

**✅ Firmado:**  
**El Jefe de Proyecto** 😎
