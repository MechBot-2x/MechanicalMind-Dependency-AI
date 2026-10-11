"""Integration tests end-to-end (V3).

Simula un usuario real: crear un proyecto multi-ecosistema y ejecutar
el flujo completo scan → diagnose → fix → verify → monitor, verificando
que la telemetría registra todo.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from mechanicalmind_ai.cli import cli

# ────────────────────────── helpers ──────────────────────────


def _make_mixed_project(root: Path) -> None:
    """Crea un proyecto multi-ecosistema (Python+Node+Go+Rust+Docker)."""
    (root / "requirements.txt").write_text("requests>=2.26.0\npyyaml>=6.0\n")
    (root / "package.json").write_text(
        json.dumps(
            {
                "name": "demo",
                "dependencies": {"express": "^4.18.0"},
                "devDependencies": {"jest": "^29.0.0"},
            }
        )
    )
    (root / "go.mod").write_text(
        "module example.com/demo\n\ngo 1.21\n\n" "require github.com/gin-gonic/gin v1.9.1\n"
    )
    (root / "Cargo.toml").write_text(
        '[package]\nname = "demo"\nversion = "0.1.0"\n\n[dependencies]\nserde = "1.0"\n'
    )
    (root / "Dockerfile").write_text("FROM python:3.11-slim\n")


class _IntegrationBase(unittest.TestCase):
    """Base: runner + tmp dir + telemetría aislada."""

    def setUp(self):
        self.runner = CliRunner()
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        _make_mixed_project(self.root)

        self._old_tel = os.environ.get("MECHMIND_TELEMETRY_PATH")
        self._old_no = os.environ.get("MECHMIND_NO_TELEMETRY")
        self.tel_path = self.root / "stats.json"
        os.environ["MECHMIND_TELEMETRY_PATH"] = str(self.tel_path)
        os.environ.pop("MECHMIND_NO_TELEMETRY", None)

    def tearDown(self):
        if self._old_tel is None:
            os.environ.pop("MECHMIND_TELEMETRY_PATH", None)
        else:
            os.environ["MECHMIND_TELEMETRY_PATH"] = self._old_tel
        if self._old_no is not None:
            os.environ["MECHMIND_NO_TELEMETRY"] = self._old_no
        self._tmp.cleanup()


# ────────────────────────── tests ──────────────────────────


class TestScanIntegration(_IntegrationBase):

    def test_scan_detects_all_ecosystems(self):
        result = self.runner.invoke(cli, ["scan", "-p", str(self.root), "-f", "json"])
        self.assertEqual(result.exit_code, 0, msg=result.output)
        data = json.loads(result.output)
        missing = {"python", "node", "go", "rust", "docker"} - set(data["ecosystems"])
        self.assertEqual(missing, set(), f"Faltan: {missing}")

    def test_scan_json_has_required_keys(self):
        result = self.runner.invoke(cli, ["scan", "-p", str(self.root), "-f", "json"])
        data = json.loads(result.output)
        for key in ("path", "ecosystems", "packages", "warnings", "summary"):
            self.assertIn(key, data)
        for pkg in data["packages"]:
            for key in ("name", "version", "ecosystem", "source"):
                self.assertIn(key, pkg)


class TestFullWorkflow(_IntegrationBase):

    def test_complete_workflow_records_telemetry(self):
        # 1. scan
        r1 = self.runner.invoke(cli, ["scan", "-p", str(self.root)])
        self.assertEqual(r1.exit_code, 0, msg=r1.output)

        # 2. diagnose
        r2 = self.runner.invoke(cli, ["diagnose", "ModuleNotFoundError: No module named 'x'"])
        self.assertEqual(r2.exit_code, 0, msg=r2.output)

        # 3. verify
        target = self.root / "requirements.txt"
        r3 = self.runner.invoke(cli, ["verify", str(target)])
        self.assertEqual(r3.exit_code, 0, msg=r3.output)
        self.assertIn("sha256:", r3.output)

        # 4. monitor --once
        r4 = self.runner.invoke(cli, ["monitor", "-p", str(self.root), "--once"])
        self.assertEqual(r4.exit_code, 0, msg=r4.output)

        # 5. telemetría
        self.assertTrue(self.tel_path.exists(), "La telemetría no se escribió")
        tel = json.loads(self.tel_path.read_text())
        for event in ("scan", "diagnose", "verify", "monitor"):
            self.assertIn(event, tel["counters"], f"Falta contador {event}")
        for eco in ("python", "node", "go", "rust", "docker"):
            self.assertIn(eco, tel["ecosystems_seen"], f"Falta ecosistema {eco}")

    @patch(
        "mechanicalmind_ai.core.utils.network_helpers.get_pypi_package_info",
        return_value={"releases": {"2.30.0": [], "2.31.0": [], "2.32.5": []}},
    )
    def test_fix_applies_version_to_requirements(self, mock_pypi):
        target = self.root / "requirements.txt"
        before = target.read_text()

        result = self.runner.invoke(
            cli,
            [
                "fix",
                "-p",
                "requests",
                "-v",
                ">=2.26.0",
                "-r",
                str(target),
                "--apply",
            ],
        )
        self.assertEqual(result.exit_code, 0, msg=result.output)

        after = target.read_text()
        self.assertNotEqual(before, after, "El archivo no cambió")
        self.assertIn("requests==2.32.5", after)
        self.assertIn("pyyaml>=6.0", after, "Se tocó un paquete que no debía")

    def test_monitor_detects_new_ecosystem(self):
        # 1er escaneo: sin php
        r1 = self.runner.invoke(cli, ["monitor", "-p", str(self.root), "--once"])
        self.assertEqual(r1.exit_code, 0, msg=r1.output)
        self.assertNotIn("monolog", r1.output)

        # Añadimos composer.json (PHP)
        (self.root / "composer.json").write_text(
            json.dumps({"require": {"monolog/monolog": "^3.0"}})
        )

        # 2º escaneo: ahora aparece
        r2 = self.runner.invoke(cli, ["monitor", "-p", str(self.root), "--once"])
        self.assertEqual(r2.exit_code, 0, msg=r2.output)
        self.assertIn("monolog", r2.output)


class TestPluginsIntegration(_IntegrationBase):

    def test_plugins_lists_all_builtins(self):
        result = self.runner.invoke(cli, ["plugins"])
        self.assertEqual(result.exit_code, 0)
        for eco in (
            "python",
            "node",
            "go",
            "rust",
            "ruby",
            "php",
            "swift",
            "docker",
            "java",
        ):
            self.assertIn(eco, result.output, f"Falta ecosistema {eco}")

    def test_plugins_detail_for_go(self):
        result = self.runner.invoke(cli, ["plugins", "go-mod"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("go.mod", result.output)


if __name__ == "__main__":
    unittest.main()
