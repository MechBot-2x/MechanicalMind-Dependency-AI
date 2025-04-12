import sys
import warnings
from pathlib import Path

# Configuración especial para Termux
project_path = str(Path(__file__).parent)
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Eliminar warnings de importación
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)
    from .dependency_analyzer import DependencyAnalyzer, main as analyzer_main
    from .error_diagnosis_engine import ErrorDiagnosisEngine
    from .auto_fix_module import DependencyAutoFixer

__all__ = ['DependencyAnalyzer', 'ErrorDiagnosisEngine', 'DependencyAutoFixer', 'analyzer_main']
