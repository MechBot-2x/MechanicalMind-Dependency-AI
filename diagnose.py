import sys
from pathlib import Path

print("=== Diagnóstico del Sistema ===")
print(f"Python path: {sys.path}")
print(f"Directorio actual: {Path.cwd()}")
print(f"¿Existe ai_core?: {(Path('ai_core') / '__init__.py').exists()}")
print(f"¿Existe dependency_analyzer?: {(Path('ai_core') / 'dependency_analyzer.py').exists()}")

try:
    from ai_core.dependency_analyzer import DependencyAnalyzer
    print("✅ Importación exitosa")
except Exception as e:
    print(f"❌ Error de importación: {str(e)}")
