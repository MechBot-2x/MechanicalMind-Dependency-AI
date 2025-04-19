import os
import unittest
from ai_core.compatibility_matrix import CompatibilityMatrix
from tempfile import NamedTemporaryFile


class TestCompatibilityMatrix(unittest.TestCase):
    def setUp(self):
        self.temp_db = NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db.name
        self.cm = CompatibilityMatrix(self.db_path)

    def tearDown(self):
        self.temp_db.close()
        os.unlink(self.db_path)

    def test_add_record_success(self):
        """Test successful addition of compatibility record"""
        result = self.cm.add_compatibility_record(
            "numpy", "1.21.0", "3.10", "compatible"
        )
        self.assertTrue(result)

    def test_add_record_failure_empty(self):
        """Test handling of empty data"""
        result = self.cm.add_compatibility_record("", "", "", "")
        self.assertFalse(result)

    def test_add_record_failure_none(self):
        """Test handling of None values"""
        result = self.cm.add_compatibility_record(None, "1.21.0", "3.10", "compatible")
        self.assertFalse(result)

    def test_check_compatibility(self):
        """Test compatibility checking"""
        self.cm.add_compatibility_record("pandas", "1.3.0", "3.9", "compatible")
        status = self.cm.check_compatibility("pandas", "1.3.0", "3.9")
        self.assertEqual(status, "compatible")

    def test_check_unknown_compatibility(self):
        """Test checking unknown package"""
        status = self.cm.check_compatibility("unknown", "1.0", "3.10")
        self.assertEqual(status, "unknown")


if __name__ == "__main__":
    unittest.main()
