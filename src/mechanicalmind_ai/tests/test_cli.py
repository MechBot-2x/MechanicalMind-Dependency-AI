"""Tests del CLI (V3)."""

import json
import tempfile
import unittest
from pathlib import Path

from click.testing import CliRunner

from mechanicalmind_ai.cli import cli


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def test_version(self):
        result = self.runner.invoke(cli, ["version"])
        self.assertEqual(result.exit_code, 0, msg=result.output)
        self.assertIn("mechmind", result.output)

    def test_help_lists_commands(self):
        result = self.runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        for cmd in ("scan", "diagnose", "fix", "verify", "version", "monitor"):
            self.assertIn(cmd, result.output)

    def test_scan_json_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "requirements.txt").write_text("requests>=2.25.1\n")
            result = self.runner.invoke(cli, ["scan", "--path", tmp, "--format", "json"])
            self.assertEqual(result.exit_code, 0, msg=result.output)
            data = json.loads(result.output)
            self.assertEqual(data["summary"]["total_packages"], 1)

    def test_scan_text_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "requirements.txt").write_text("requests>=2.25.1\n")
            result = self.runner.invoke(cli, ["scan", "--path", tmp])
            self.assertEqual(result.exit_code, 0, msg=result.output)
            self.assertIn("requests", result.output)

    def test_diagnose_runs(self):
        result = self.runner.invoke(cli, ["diagnose", "ModuleNotFoundError: No module named 'foo'"])
        self.assertEqual(result.exit_code, 0, msg=result.output)
        self.assertIn("Diagnóstico", result.output)

    def test_verify_sha256(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            f.write("hola\n")
            path = f.name
        result = self.runner.invoke(cli, ["verify", path, "-a", "sha256"])
        self.assertEqual(result.exit_code, 0, msg=result.output)
        self.assertIn("sha256:", result.output)

    def test_fix_runs(self):
        result = self.runner.invoke(
            cli,
            ["fix", "--error-type", "VERSION_NOT_FOUND", "--package", "requests"],
        )
        self.assertEqual(result.exit_code, 0, msg=result.output)
        self.assertIn("Auto-Fix", result.output)

    def test_monitor_stub(self):
        result = self.runner.invoke(cli, ["monitor"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("roadmap", result.output)


if __name__ == "__main__":
    unittest.main()
