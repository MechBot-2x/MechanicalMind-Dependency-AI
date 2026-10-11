"""Tests de ProjectScanner (V3)."""

import json
import tempfile
import unittest
from pathlib import Path

from mechanicalmind_ai.core.scanner import Package, ProjectScanner


class TestProjectScanner(unittest.TestCase):

    def test_scan_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = ProjectScanner(tmp).scan()
            self.assertEqual(result.summary["total_packages"], 0)
            self.assertEqual(result.summary["total_files"], 0)
            self.assertEqual(result.ecosystems, [])

    def test_scan_nonexistent_path(self):
        result = ProjectScanner("/ruta/que/no/existe/abc123").scan()
        self.assertTrue(result.warnings)
        self.assertEqual(result.summary["total_packages"], 0)

    def test_scan_requirements_txt(self):
        with tempfile.TemporaryDirectory() as tmp:
            req = Path(tmp) / "requirements.txt"
            req.write_text("requests>=2.25.1\npyyaml>=6.0\n# comentario\n\n")
            result = ProjectScanner(tmp).scan()
            self.assertEqual(result.summary["total_packages"], 2)
            self.assertIn("python", result.ecosystems)
            names = [p.name for p in result.packages]
            self.assertIn("requests", names)
            self.assertIn("pyyaml", names)

    def test_scan_package_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            pkg = Path(tmp) / "package.json"
            pkg.write_text(
                json.dumps(
                    {
                        "dependencies": {"express": "^4.18.0"},
                        "devDependencies": {"jest": "^29.0.0"},
                    }
                )
            )
            result = ProjectScanner(tmp).scan()
            self.assertEqual(result.summary["total_packages"], 2)
            self.assertIn("node", result.ecosystems)

    def test_scan_pyproject(self):
        with tempfile.TemporaryDirectory() as tmp:
            pp = Path(tmp) / "pyproject.toml"
            pp.write_text(
                '[project]\nname = "demo"\nversion = "0.1.0"\n'
                'dependencies = ["requests>=2.25", "pyyaml>=6.0"]\n'
            )
            result = ProjectScanner(tmp).scan()
            self.assertEqual(result.summary["total_packages"], 2)
            self.assertIn("python", result.ecosystems)

    def test_scan_dockerfile(self):
        with tempfile.TemporaryDirectory() as tmp:
            df = Path(tmp) / "Dockerfile"
            df.write_text("FROM python:3.11-slim\nRUN pip install requests\n")
            result = ProjectScanner(tmp).scan()
            self.assertEqual(result.summary["total_packages"], 1)
            self.assertEqual(result.packages[0].name, "python")
            self.assertEqual(result.packages[0].version, "3.11-slim")
            self.assertIn("docker", result.ecosystems)

    def test_scan_multi_ecosystem(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "requirements.txt").write_text("requests>=2.25\n")
            (Path(tmp) / "package.json").write_text(
                json.dumps({"dependencies": {"express": "^4.18"}})
            )
            result = ProjectScanner(tmp).scan()
            self.assertEqual(result.summary["total_packages"], 2)
            self.assertIn("python", result.ecosystems)
            self.assertIn("node", result.ecosystems)

    def test_to_dict_serializable(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "requirements.txt").write_text("requests>=2.25\n")
            d = ProjectScanner(tmp).scan().to_dict()
            self.assertIsInstance(d, dict)
            self.assertIn("packages", d)
            json.dumps(d)  # no debe lanzar


if __name__ == "__main__":
    unittest.main()
