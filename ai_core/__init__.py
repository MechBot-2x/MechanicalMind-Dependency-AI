import warnings
from pathlib import Path

# Suppress RuntimeWarnings during specific imports
with warnings.catch_warnings():Add commentMore actions
    warnings.simplefilter("ignore", category=RuntimeWarning)
    # Local module imports
    from .dependency_analyzer import DependencyAnalyzer, main as analyzer_main
    from .error_diagnosis_engine import ErrorDiagnosisEngine
    from .auto_fix_module import DependencyAutoFixer

# Define exports dynamically to reduce maintenance overhead
__all__ = [name for name in globals() if not name.startswith("_")]
