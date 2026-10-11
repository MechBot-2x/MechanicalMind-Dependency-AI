"""Tests de DependencyAnalyzer (V3)."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from mechanicalmind_ai.core.analyzer import DependencyAnalyzer


class TestDependencyAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = DependencyAnalyzer()

    def test_parse_requirements_txt_ignores_comments_and_blanks(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("numpy>=1.19.0,<2.0.0\n")
            f.write("pandas==1.3.0\n")
            f.write("# comentario\n")
            f.write("\n")
            f.write("   \n")
            path = f.name

        result = self.analyzer.parse_requirements_txt(path)
        self.assertEqual(len(result), 2)
        self.assertIn("numpy>=1.19.0,<2.0.0", result)
        self.assertIn("pandas==1.3.0", result)

    @patch("subprocess.run")
    def test_get_package_dependencies_calls_pip_show(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Name: numpy\nVersion: 1.21.0\nRequires: pandas, scipy"
        mock_run.return_value = mock_result

        result = self.analyzer._get_package_dependencies("numpy")

        self.assertIn("Name: numpy", result)
        self.assertIn("Version: 1.21.0", result)
        mock_run.assert_called_once_with(
            ["pip", "show", "numpy"],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_analyze_returns_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.analyzer.analyze(tmp)
            self.assertEqual(result["status"], "success")
            self.assertTrue(result["exists"])

    def test_analyze_nonexistent_path(self):
        result = self.analyzer.analyze("/ruta/que/no/existe/xyz")
        self.assertEqual(result["status"], "success")
        self.assertFalse(result["exists"])


if __name__ == "__main__":
    unittest.main()
