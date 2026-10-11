# Guía de contribución

¡Gracias por tu interés en MechMind AI! Esta guía explica cómo contribuir
de forma que tu PR se integre sin fricción.

## Requisitos del proyecto

- **Python 3.11+** (probado en 3.11, 3.12 y 3.14).
- Familiaridad básica con `git`, `pip` y entornos virtuales.
- No se requiere conocimiento previo del dominio.

## Configurar el entorno

```bash
git clone https://github.com/MechBot-2x/MechanicalMind-Dependency-AI.git
cd MechanicalMind-Dependency-AI
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -e ".[dev,test]"
```

Comandos de desarrollo

Comando Qué hace
bash scripts/lint.sh ruff + black + pytest en una pasada
ruff check src Solo lint
black src Solo formato
pytest Solo tests
mechmind --help Ver los comandos disponibles

Antes de subir un PR, asegúrate de que bash scripts/lint.sh pasa sin errores.

Cómo contribuir

Reportar bugs

Abre un issue
con:

· Qué esperabas que pasara.
· Qué pasó en realidad (con el output completo).
· Cómo reproducirlo (comandos exactos).
· Versión: python --version y mechmind --version.

Proponer features

Abre un issue con la etiqueta enhancement describiendo:

· El caso de uso real que resuelve.
· Cómo lo usarías (mechmind ...).
· Alternativas que has considerado.

Enviar código

1. Fork del repositorio.
2. Crea una rama descriptiva:
   ```bash
   git checkout -b feat/nombre-corto
   # o
   git checkout -b fix/nombre-del-bug
   ```
3. Haz tus cambios con tests. Un PR sin tests casi nunca se acepta.
4. Asegúrate de que pasa el lint:
   ```bash
   bash scripts/lint.sh
   ```
5. Commit con mensaje claro (ver abajo).
6. Push y abre un Pull Request describiendo el "qué" y el "por qué".

Estilo de commits

Usamos Conventional Commits:

```
feat(scope): descripción corta
fix(scope): descripción corta
chore(scope): descripción corta
test(scope): descripción corta
docs(scope): descripción corta
refactor(scope): descripción corta
```

Ejemplos reales de este repo:

```
feat(monitor): comando monitor real + tests con mocks
fix: repara regex Swift + implementa plugins CLI
chore: elimina requirements viejos y workflows basura
test(integration): flujo end-to-end multi-ecosystem
```

Estilo de código

· Python: PEP 8 + Black (line-length 100).
· Imports: ordenados con isort (perfil black).
· Tipos: anotaciones en funciones públicas.
· Docstrings: estilo reStructuredText o Google en clases y funciones
  importantes.
· Tests: unittest (los .py actuales) o pytest (compatible).

No uses dependencias nuevas sin justificarlo en el PR.

Añadir soporte para un nuevo ecosistema

El scanner usa un registro de parsers. Añadir uno nuevo es trivial:

1. Crea un archivo src/mechanicalmind_ai/core/plugins/mi_formato.py:
   ```python
   from pathlib import Path
   from ..models import Package
   from .registry import Parser
   
   def _parse_mi_formato(path: Path) -> list[Package]:
       pkgs = []
       # ... parsear path ...
       pkgs.append(Package(name="...", version="...", ecosystem="mi_eco", source=str(path)))
       return pkgs
   
   PARSER = Parser(
       name="mi-eco-formato",
       ecosystem="mi_eco",
       description="Mi formato (mi herramienta)",
       filename_patterns=("mi.manifest",),
       parse=_parse_mi_formato,
   )
   ```
2. Añádelo a BUILTIN_PARSERS en core/plugins/builtin.py.
3. Añade un test en src/mechanicalmind_ai/tests/test_scanner.py con un
   fixture temporal.
4. Actualiza la tabla de ecosistemas en README.md.

Los terceros también pueden registrar parsers sin tocar el core:

```python
from mechanicalmind_ai.core.plugins import Parser, register_parser

register_parser(Parser(...))
```

Tests

· Ubicación: src/mechanicalmind_ai/tests/
· Runner: pytest (configurado en pyproject.toml).
· Timeout: 20s por test (configurado).
· Cobertura: sin mínimo obligatorio, pero se esperan tests unitarios
  para nueva lógica y al menos un test de integración si toca el CLI.

Buenos ejemplos existentes:

· test_scanner.py — parsers.
· test_cli.py — comandos con CliRunner.
· test_integration.py — flujo completo multi-ecosistema.

Accesibilidad

· Usa nombres descriptivos, no abreviaturas crípticas.
· Comentarios en español o inglés, coherentes con el archivo.
· Evita jerga innecesaria en mensajes de error al usuario.

Seguridad

· Nunca incluyas credenciales, tokens o claves API en un PR.
· La telemetría es local-only; no añadas llamadas a servicios externos
  sin discutirlo en un issue primero.
· Si encuentras una vulnerabilidad, escríbenos en privado antes de abrir
  un issue público.

Licencia

Al contribuir aceptas que tus aportes se licencien bajo Apache 2.0
(ver LICENSE).

¿Dudas?

Abre un issue
o una discussion.
¡Gracias por contribuir! 🚀
