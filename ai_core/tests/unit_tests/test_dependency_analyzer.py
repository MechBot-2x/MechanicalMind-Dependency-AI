import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from ai_core.dependency_analyzer import DependencyAnalyzer


class TestDependencyAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data_dir = Path(__file__).parent / "test_data"
        cls.test_data_dir.mkdir(exist_ok=True)

        # Crear archivo de prueba con dependencias complejas
        cls.test_file = cls.test_data_dir / "requirements_sample.txt"
        with open(cls.test_file, "w") as f:
            f.write("numpy>=1.19.0,<2.0.0\npandas==1.3.0\n# Comentario\n\n")

    def setUp(self):
        self.analyzer = DependencyAnalyzer()

    def test_parse_requirements_txt(self):
        """Test para parse_requirements_txt con versiones"""
        result = self.analyzer.parse_requirements_txt(self.test_file)
        self.assertEqual(len(result), 2)
        self.assertIn("numpy>=1.19.0,<2.0.0", result)
        self.assertIn("pandas==1.3.0", result)
        self.assertNotIn("# Comentario", result)

    @patch("subprocess.run")
    def test_get_package_dependencies(self, mock_run):
        """Test mockeado para _get_package_dependencies"""
        # Configurar mock
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Name: numpy\nVersion: 1.21.0\nRequires: pandas, scipy"
        mock_run.return_value = mock_result

        # Ejecutar prueba
        result = self.analyzer._get_package_dependencies("numpy")

        # Verificar resultados
        self.assertIn("Name: numpy", result)
        self.assertIn("Version: 1.21.0", result)
        self.assertIn("Requires: pandas, scipy", result)
        mock_run.assert_called_once_with(
            ["pip", "show", "numpy"], capture_output=True, text=True
        )

    def test_analyze_method(self):
        """Test para el método analyze"""
        test_path = "/fake/path/to/project"
        result = self.analyzer.analyze(test_path)
        self.assertEqual(result["status"], "success")


if __name__ == "__main__":
    unittest.main()
