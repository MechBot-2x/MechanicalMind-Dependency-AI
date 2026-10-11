# Changelog

Todos los cambios notables de este proyecto se documentan aquí.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto se adhiere a [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

### Por añadir
- `mechmind doctor` — diagnóstico del entorno (Python, pip, git, venv, red).
- Soporte para `requirements.yaml`, `.nvmrc`, `.python-version`, `.tool-versions`.
- `mechmind scan --fix-all` — corrección masiva de versiones fuera de rango.

---

## [3.0.1] — 2025-10-11

### Añadido
- **CLI multi-comando** con 8 comandos: `scan`, `diagnose`, `fix`, `verify`,
  `monitor`, `plugins`, `learn`, `version`.
- **`ProjectScanner` multi-ecosystem** con 10 parsers registrados:
  python (requirements.txt + pyproject.toml), node, java, docker, go, rust,
  ruby, php, swift.
- **Sistema de plugins** con `ParserRegistry` y API pública
  (`register_parser`, `unregister_parser`, `list_parsers`).
- **`DependencyMonitor`** — watcher con `run_once()` y `watch(interval, on_change)`.
  CLI: `mechmind monitor --path DIR --interval S --once`.
- **`TelemetryStore`** — estadísticas de uso locales en `~/.mechmind/stats.json`.
  Respeta `MECHMIND_TELEMETRY_PATH` y `MECHMIND_NO_TELEMETRY=1`.
- **`mechmind fix --apply`** — escribe cambios en `requirements.txt`
  (por defecto solo recomienda).
- **Tests de integración** end-to-end con proyecto multi-ecosistema simulado.
- **CI GitHub Actions** en Python 3.11 y 3.12 con ruff + black + pytest.

### Cambiado
- **`pyproject.toml` unificado** con metadatos, dependencias, entry_points y
  configuración de herramientas (antes había un `requirements.txt` con
  contenido TOML por error).
- **Estructura del paquete** consolidada en `src/mechanicalmind_ai/`
  (antes había V2 y V3 mezclados en `ai_core/`, `src/mechanicalmind/`).
- **`DependencyAutoFixer`** es defensivo: `apply_fix` no propaga excepciones.
- **Versiones ordenadas semánticamente** con `packaging.version.Version`
  (antes usaba `sorted()` sobre strings → `2.9.2 > 2.32.0`).

### Corregido
- `import datetime` faltante en `error_diagnosis_engine.py`.
- `_fix_distribution_unavailable` y `_generic_fix` ausentes en
  `DependencyAutoFixer`.
- Regex de Swift en `builtin.py` roto por comillas triples anidadas.
- 6 tests de `TelemetryStore` afectados por un side-effect global de
  `MECHMIND_NO_TELEMETRY`.

### Eliminado
- `ai_core/` (V2 completo), `dependency_analyzer.py`, `tests/` de V2,
  `scripts/*` de V2.
- `requirements.fixed.txt`, `requirements-dev.txt`, `requeriments.docs.txt`,
  `filtered_reqs.txt` (todo migrado a `pyproject.toml`).
- Workflows con nombres basura generados por AI
  (`TACTICAL_STATUS_REPORT`, `LAUNCH AI SCAN MISSILE`, etc.).
- Symlink `data` del tracking de git (rompía Jekyll en CI).

---

## [3.0.0] — 2025-10-10

### Añadido
- Reescritura completa del motor de diagnóstico (`ErrorDiagnosisEngine`).
- `CompatibilityMatrix` con SQLite para compatibilidades Python↔versión.
- `DependencyAnalyzer` y `DependencyAutoFixer`.
- `ProjectScanner` inicial (Python + Node + Java + Docker).
- CLI básico con `mechmind ERROR_LOG`.

### Cambiado
- Migración a `src/mechanicalmind_ai/` como layout estándar.

---

## [2.0.0] — 2024-XX-XX

- Versión histórica. Ver commits anteriores en el repositorio.

[Unreleased]: https://github.com/MechBot-2x/MechanicalMind-Dependency-AI/compare/v3.0.1...HEAD
[3.0.1]: https://github.com/MechBot-2x/MechanicalMind-Dependency-AI/compare/v3.0.0...v3.0.1
[3.0.0]: https://github.com/MechBot-2x/MechanicalMind-Dependency-AI/releases/tag/v3.0.0
[2.0.0]: https://github.com/MechBot-2x/MechanicalMind-Dependency-AI/releases/tag/v2.0.0
