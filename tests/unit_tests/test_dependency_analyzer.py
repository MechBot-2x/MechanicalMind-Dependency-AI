import unittest
from pathlib import Path
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
        """Test para parse_requirements_txt"""
        result = self.analyzer.parse_requirements_txt(self.test_file)
        self.assertEqual(len(result), 2)
        self.assertIn("numpy", result)
        self.assertIn("pandas", result)
        self.assertNotIn("# Esto es un comentario", result)

    def test_get_package_dependencies(self):
        """Test para _get_package_dependencies"""
        result = self.analyzer._get_package_dependencies("pip")
        self.assertTrue("Name: pip" in result or "Error" in result)


if __name__ == "__main__":
    unittest.main()
