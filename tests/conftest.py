from unittest.mock import MagicMock
import pytest
from ai_core.dependency_analyzer import DependencyAnalyzer


@pytest.fixture
def mock_analyzer():
    analyzer = DependencyAnalyzer()
    analyzer._get_package_dependencies = MagicMock(return_value={})
    return analyzer
