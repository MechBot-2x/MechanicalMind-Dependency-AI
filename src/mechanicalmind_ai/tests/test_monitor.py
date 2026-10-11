"""Tests de DependencyMonitor (V3)."""

import tempfile
import time
import unittest
from pathlib import Path

from mechanicalmind_ai.core.monitor import ChangeSet, DependencyMonitor


class TestDependencyMonitor(unittest.TestCase):

    def test_initial_snapshot_reports_added(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "requirements.txt").write_text("requests>=2.26\n")
            mon = DependencyMonitor(tmp)
            changes = mon.run_once()
            # En el primer escaneo todo es "added"
            self.assertEqual(len(changes.added), 1)
            self.assertEqual(changes.added[0].name, "requests")

    def test_no_changes_on_second_scan(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "requirements.txt").write_text("requests>=2.26\n")
            mon = DependencyMonitor(tmp)
            mon.run_once()  # primer escaneo
            changes = mon.run_once()  # sin cambios
            self.assertTrue(changes.is_empty)

    def test_detects_added_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            req = Path(tmp) / "requirements.txt"
            req.write_text("requests>=2.26\n")
            mon = DependencyMonitor(tmp)
            mon.run_once()

            time.sleep(0.05)  # asegurar mtime distinto
            req.write_text("requests>=2.26\npyyaml>=6.0\n")
            changes = mon.run_once()

            self.assertEqual(len(changes.added), 1)
            self.assertEqual(changes.added[0].name, "pyyaml")

    def test_detects_removed_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            req = Path(tmp) / "requirements.txt"
            req.write_text("requests>=2.26\npyyaml>=6.0\n")
            mon = DependencyMonitor(tmp)
            mon.run_once()

            time.sleep(0.05)
            req.write_text("requests>=2.26\n")
            changes = mon.run_once()

            self.assertEqual(len(changes.removed), 1)
            self.assertEqual(changes.removed[0].name, "pyyaml")

    def test_detects_version_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            req = Path(tmp) / "requirements.txt"
            req.write_text("requests>=2.20\n")
            mon = DependencyMonitor(tmp)
            mon.run_once()

            time.sleep(0.05)
            req.write_text("requests>=2.26\n")
            changes = mon.run_once()

            self.assertEqual(len(changes.changed), 1)
            old, new = changes.changed[0]
            self.assertEqual(old.name, "requests")
            self.assertEqual(old.version, ">=2.20")
            self.assertEqual(new.version, ">=2.26")

    def test_changeset_to_dict(self):
        cs = ChangeSet()
        self.assertTrue(cs.is_empty)
        d = cs.to_dict()
        self.assertIn("added", d)
        self.assertIn("removed", d)
        self.assertIn("changed", d)


if __name__ == "__main__":
    unittest.main()
