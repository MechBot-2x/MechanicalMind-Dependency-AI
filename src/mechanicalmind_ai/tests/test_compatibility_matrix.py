"""Tests de CompatibilityMatrix (V3)."""

import tempfile
import unittest
from pathlib import Path

from mechanicalmind_ai.core.compatibility_matrix import CompatibilityMatrix


class TestCompatibilityMatrix(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        self.matrix = CompatibilityMatrix(db_path=self.tmp.name)

    def tearDown(self):
        Path(self.tmp.name).unlink(missing_ok=True)

    def test_instantiable(self):
        self.assertIsNotNone(self.matrix)

    def test_add_and_check_compatibility(self):
        self.matrix.add_compatibility_record(
            package="requests",
            version="2.32.0",
            python_version="3.11",
            status="compatible",
        )
        result = self.matrix.check_compatibility(
            package="requests",
            version="2.32.0",
            python_version="3.11",
        )
        self.assertIsNotNone(result)

    def test_find_compatible_versions_returns_list(self):
        versions = self.matrix.find_compatible_versions(package="requests", python_version="3.11")
        self.assertIsInstance(versions, list)


if __name__ == "__main__":
    unittest.main()
