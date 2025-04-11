"""
MechanicalMind Dependency AI Core Package v2.0
Main package initialization file
"""

from .dependency_analyzer import DependencyAnalyzer
from .error_diagnosis_engine import ErrorDiagnosisEngine
from .auto_fix_module import DependencyAutoFixer
from .compatibility_matrix import CompatibilityMatrix

__version__ = "2.0.1"
__all__ = [
    'DependencyAnalyzer',
    'ErrorDiagnosisEngine',
    'DependencyAutoFixer',
    'CompatibilityMatrix'
]
