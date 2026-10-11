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

    def test_scan_go_mod(self):
        with tempfile.TemporaryDirectory() as tmp:
            go_mod = Path(tmp) / "go.mod"
            go_mod.write_text(
                "module example.com/foo\n"
                "\n"
                "go 1.21\n"
                "\n"
                "require (\n"
                "    github.com/gin-gonic/gin v1.9.1\n"
                "    golang.org/x/text v0.12.0\n"
                ")\n"
                "\n"
                "require github.com/single/one v2.0.0\n"
            )
            result = ProjectScanner(tmp).scan()
            self.assertIn("go", result.ecosystems)
            names = [p.name for p in result.packages]
            self.assertIn("github.com/gin-gonic/gin", names)
            self.assertIn("golang.org/x/text", names)
            self.assertIn("github.com/single/one", names)
            self.assertEqual(result.summary["total_packages"], 3)

    def test_scan_cargo_toml(self):
        with tempfile.TemporaryDirectory() as tmp:
            cargo = Path(tmp) / "Cargo.toml"
            cargo.write_text(
                "[package]\n"
                'name = "demo"\n'
                'version = "0.1.0"\n'
                "\n"
                "[dependencies]\n"
                'serde = "1.0"\n'
                'tokio = { version = "1.35", features = ["full"] }\n'
                "\n"
                "[dev-dependencies]\n"
                'criterion = "0.5"\n'
            )
            result = ProjectScanner(tmp).scan()
            self.assertIn("rust", result.ecosystems)
            names = [p.name for p in result.packages]
            self.assertIn("serde", names)
            self.assertIn("tokio", names)
            self.assertIn("criterion", names)

    def test_scan_gemfile(self):
        with tempfile.TemporaryDirectory() as tmp:
            gemfile = Path(tmp) / "Gemfile"
            gemfile.write_text(
                'source "https://rubygems.org"\n'
                'gem "rails", "~> 7.0"\n'
                'gem "pg"\n'
                'gem "puma", ">= 5.0"\n'
                '# gem "commented"\n'
            )
            result = ProjectScanner(tmp).scan()
            self.assertIn("ruby", result.ecosystems)
            names = [p.name for p in result.packages]
            self.assertIn("rails", names)
            self.assertIn("pg", names)
            self.assertIn("puma", names)
            self.assertNotIn("commented", names)

    def test_scan_composer_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            composer = Path(tmp) / "composer.json"
            composer.write_text(
                "{\n"
                '  "require": {\n'
                '    "php": ">=8.0",\n'
                '    "monolog/monolog": "^3.0"\n'
                "  },\n"
                '  "require-dev": {\n'
                '    "phpunit/phpunit": "^10.0"\n'
                "  }\n"
                "}\n"
            )
            result = ProjectScanner(tmp).scan()
            self.assertIn("php", result.ecosystems)
            names = [p.name for p in result.packages]
            self.assertIn("monolog/monolog", names)
            self.assertIn("phpunit/phpunit", names)

    def test_scan_swift_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            swift = Path(tmp) / "Package.swift"
            swift.write_text(
                "let package = Package(\n"
                '    name: "MyLib",\n'
                "    dependencies: [\n"
                '        .package(url: "https://github.com/apple/swift-nio.git", from: "2.0.0"),\n'
                '        .package(url: "https://github.com/vapor/vapor.git", from: "4.0.0")\n'
                "    ]\n"
                ")\n"
            )
            result = ProjectScanner(tmp).scan()
            self.assertIn("swift", result.ecosystems)
            names = [p.name for p in result.packages]
            self.assertIn("swift-nio", names)
            self.assertIn("vapor", names)

    def test_scan_multi_language(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "requirements.txt").write_text("requests>=2.26\n")
            (Path(tmp) / "go.mod").write_text("module x\n\nrequire github.com/foo/bar v1.0.0\n")
            (Path(tmp) / "Cargo.toml").write_text('[dependencies]\nserde = "1.0"\n')
            result = ProjectScanner(tmp).scan()
            for eco in ("python", "go", "rust"):
                self.assertIn(eco, result.ecosystems)

    def test_scan_go_mod(self):
        with tempfile.TemporaryDirectory() as tmp:
            go_mod = Path(tmp) / "go.mod"
            go_mod.write_text(
                "module example.com/foo\n"
                "\n"
                "go 1.21\n"
                "\n"
                "require (\n"
                "    github.com/gin-gonic/gin v1.9.1\n"
                "    golang.org/x/text v0.12.0\n"
                ")\n"
                "\n"
                "require github.com/single/one v2.0.0\n"
            )
            result = ProjectScanner(tmp).scan()
            self.assertIn("go", result.ecosystems)
            names = [p.name for p in result.packages]
            self.assertIn("github.com/gin-gonic/gin", names)
            self.assertIn("golang.org/x/text", names)
            self.assertIn("github.com/single/one", names)
            self.assertEqual(result.summary["total_packages"], 3)

    def test_scan_cargo_toml(self):
        with tempfile.TemporaryDirectory() as tmp:
            cargo = Path(tmp) / "Cargo.toml"
            cargo.write_text(
                "[package]\n"
                'name = "demo"\n'
                'version = "0.1.0"\n'
                "\n"
                "[dependencies]\n"
                'serde = "1.0"\n'
                'tokio = { version = "1.35", features = ["full"] }\n'
                "\n"
                "[dev-dependencies]\n"
                'criterion = "0.5"\n'
            )
            result = ProjectScanner(tmp).scan()
            self.assertIn("rust", result.ecosystems)
            names = [p.name for p in result.packages]
            self.assertIn("serde", names)
            self.assertIn("tokio", names)
            self.assertIn("criterion", names)

    def test_scan_gemfile(self):
        with tempfile.TemporaryDirectory() as tmp:
            gemfile = Path(tmp) / "Gemfile"
            gemfile.write_text(
                'source "https://rubygems.org"\n'
                'gem "rails", "~> 7.0"\n'
                'gem "pg"\n'
                'gem "puma", ">= 5.0"\n'
                '# gem "commented"\n'
            )
            result = ProjectScanner(tmp).scan()
            self.assertIn("ruby", result.ecosystems)
            names = [p.name for p in result.packages]
            self.assertIn("rails", names)
            self.assertIn("pg", names)
            self.assertIn("puma", names)
            self.assertNotIn("commented", names)

    def test_scan_composer_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            composer = Path(tmp) / "composer.json"
            composer.write_text(
                "{\n"
                '  "require": {\n'
                '    "php": ">=8.0",\n'
                '    "monolog/monolog": "^3.0"\n'
                "  },\n"
                '  "require-dev": {\n'
                '    "phpunit/phpunit": "^10.0"\n'
                "  }\n"
                "}\n"
            )
            result = ProjectScanner(tmp).scan()
            self.assertIn("php", result.ecosystems)
            names = [p.name for p in result.packages]
            self.assertIn("monolog/monolog", names)
            self.assertIn("phpunit/phpunit", names)

    def test_scan_swift_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            swift = Path(tmp) / "Package.swift"
            swift.write_text(
                "let package = Package(\n"
                '    name: "MyLib",\n'
                "    dependencies: [\n"
                '        .package(url: "https://github.com/apple/swift-nio.git", from: "2.0.0"),\n'
                '        .package(url: "https://github.com/vapor/vapor.git", from: "4.0.0")\n'
                "    ]\n"
                ")\n"
            )
            result = ProjectScanner(tmp).scan()
            self.assertIn("swift", result.ecosystems)
            names = [p.name for p in result.packages]
            self.assertIn("swift-nio", names)
            self.assertIn("vapor", names)

    def test_scan_multi_language(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "requirements.txt").write_text("requests>=2.26\n")
            (Path(tmp) / "go.mod").write_text("module x\n\nrequire github.com/foo/bar v1.0.0\n")
            (Path(tmp) / "Cargo.toml").write_text('[dependencies]\nserde = "1.0"\n')
            result = ProjectScanner(tmp).scan()
            for eco in ("python", "go", "rust"):
                self.assertIn(eco, result.ecosystems)


if __name__ == "__main__":
    unittest.main()
