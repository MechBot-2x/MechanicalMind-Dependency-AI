import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")

from ai_core.dependency_analyzer import DependencyAnalyzer

__all__ = ['DependencyAnalyzer']
