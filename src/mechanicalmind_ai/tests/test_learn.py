"""Tests de TelemetryStore y del comando learn (V3)."""

import json
import os
import tempfile
import unittest
from pathlib import Path

from click.testing import CliRunner

from mechanicalmind_ai.cli import cli
from mechanicalmind_ai.core.learn import TelemetryStore


class TestTelemetryStore(unittest.TestCase):

    def setUp(self):
        # Aislar de la telemetría configurada por otros tests
        self._old_path = os.environ.pop("MECHMIND_TELEMETRY_PATH", None)
        self._old_no_tel = os.environ.pop("MECHMIND_NO_TELEMETRY", None)

        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.path = Path(self.tmp.name)
        self.path.unlink()  # aseguramos que arranca vacío
        self.store = TelemetryStore(path=self.path)

    def tearDown(self):
        if self.path.exists():
            self.path.unlink()
        if self._old_path is not None:
            os.environ["MECHMIND_TELEMETRY_PATH"] = self._old_path
        if self._old_no_tel is not None:
            os.environ["MECHMIND_NO_TELEMETRY"] = self._old_no_tel

    def test_empty_stats(self):
        data = self.store.get_stats()
        self.assertEqual(data["counters"], {})
        self.assertEqual(data["ecosystems_seen"], [])

    def test_record_increments_counter(self):
        self.store.record("scan")
        self.store.record("scan")
        self.store.record("diagnose")
        data = self.store.get_stats()
        self.assertEqual(data["counters"]["scan"], 2)
        self.assertEqual(data["counters"]["diagnose"], 1)

    def test_record_tracks_ecosystems(self):
        self.store.record("scan", ecosystems=["python", "node"])
        self.store.record("scan", ecosystems=["node", "go"])
        data = self.store.get_stats()
        self.assertEqual(data["ecosystems_seen"], ["go", "node", "python"])

    def test_record_tracks_packages(self):
        self.store.record(
            "scan",
            packages=[
                {"name": "requests", "ecosystem": "python"},
                {"name": "requests", "ecosystem": "python"},
                {"name": "express", "ecosystem": "node"},
            ],
        )
        data = self.store.get_stats()
        self.assertEqual(data["packages_seen"]["python"]["requests"], 2)
        self.assertEqual(data["packages_seen"]["node"]["express"], 1)

    def test_reset_removes_file(self):
        self.store.record("scan")
        self.assertTrue(self.path.exists())
        self.store.reset()
        self.assertFalse(self.path.exists())

    def test_export_json(self):
        self.store.record("scan", ecosystems=["python"])
        out = self.store.export("json")
        data = json.loads(out)
        self.assertEqual(data["counters"]["scan"], 1)

    def test_export_csv(self):
        self.store.record("scan")
        self.store.record("diagnose")
        out = self.store.export("csv")
        self.assertIn("counter,scan,1", out)
        self.assertIn("counter,diagnose,1", out)

    def test_export_unknown_format(self):
        with self.assertRaises(ValueError):
            self.store.export("xml")

    def test_atomic_write_uses_tmp(self):
        self.store.record("scan")
        # No debe quedar el .tmp tras un save correcto
        self.assertFalse(self.path.with_suffix(self.path.suffix + ".tmp").exists())


class TestLearnCLI(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self._old_tel = os.environ.get("MECHMIND_TELEMETRY_PATH")
        self._old_no = os.environ.get("MECHMIND_NO_TELEMETRY")

        # Aislar en un directorio temporal propio
        self.tmp_dir = tempfile.mkdtemp()
        self.tel_path = Path(self.tmp_dir) / "stats.json"
        os.environ["MECHMIND_TELEMETRY_PATH"] = str(self.tel_path)
        os.environ.pop("MECHMIND_NO_TELEMETRY", None)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.tmp_dir, ignore_errors=True)
        if self._old_tel is None:
            os.environ.pop("MECHMIND_TELEMETRY_PATH", None)
        else:
            os.environ["MECHMIND_TELEMETRY_PATH"] = self._old_tel
        if self._old_no is not None:
            os.environ["MECHMIND_NO_TELEMETRY"] = self._old_no

    def test_learn_path(self):
        result = self.runner.invoke(cli, ["learn", "path"])
        self.assertEqual(result.exit_code, 0)
        # Debe reportar la ruta que hemos forzado
        self.assertEqual(result.output.strip(), str(self.tel_path))

    def test_learn_reset_requires_yes(self):
        result = self.runner.invoke(cli, ["learn", "reset"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("--yes", result.output)

    def test_learn_export_json_to_file(self):
        out = Path(self.tmp_dir) / "export.json"
        result = self.runner.invoke(cli, ["learn", "export", "-f", "json", "-o", str(out)])
        self.assertEqual(result.exit_code, 0, msg=result.output)
        self.assertTrue(out.exists())
        self.assertIn("version", out.read_text())


if __name__ == "__main__":
    unittest.main()
