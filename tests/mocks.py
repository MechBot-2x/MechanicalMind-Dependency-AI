from unittest.mock import MagicMock
from ai_core.dependency_analyzer import DependencyAnalyzer

def get_mock_analyzer():
    analyzer = DependencyAnalyzer()
    analyzer._get_package_dependencies = MagicMock(return_value="mock_data")
    return analyzer
