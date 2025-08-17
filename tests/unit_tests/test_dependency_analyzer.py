import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from ai_core.dependency_analyzer import DependencyAnalyzer


class TestDependencyAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = DependencyAnalyzer()
        self.test_data_dir = Path(__file__).parent / "test_data"
        self.test_data_dir.mkdir(exist_ok=True)

    # Ejemplo de test adicional para edge cases
    def test_empty_requirements_file(self):
        empty_file = self.test_data_dir / "empty.txt"
        empty_file.touch()
        result = self.analyzer.parse_requirements_txt(empty_file)
        self.assertEqual(len(result), 0)

        # Crear archivo de prueba
        self.test_file = self.test_data_dir / "requirements_sample.txt"
        with open(self.test_file, "w") as f:
            f.write("numpy\npandas\n# Esto es un comentario\n\n")


    def test_parse_requirements_txt(self):
        """Test parsing standard requirements.txt"""
        analyzer = DependencyAnalyzer()
        test_file = self.test_data_dir / "requirements_sample.txt"
        
        with patch.object(analyzer, '_get_package_dependencies') as mock_deps:
            mock_deps.return_value = {}
            analyzer._parse_dependencies(test_file)
            
        self.assertIn("numpy", analyzer.dependency_graph)
        self.assertEqual(
            analyzer.dependency_graph["numpy"]["version"], 
            ">=1.19.0,<2.0.0"
        )
    
    @patch('subprocess.run')
    def test_package_dependencies(self, mock_run):
        """Test getting package dependencies"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Requires: pandas, scipy\nVersion: 1.2.3"
        mock_run.return_value = mock_result
        
        analyzer = DependencyAnalyzer()
        deps = analyzer._get_package_dependencies("numpy")
        
        self.assertIn("pandas", deps)
        self.assertIn("scipy", deps)
    
    # [...] Additional test cases
if __name__ == '__main__':