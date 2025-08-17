import unittest
import sqlite3
from unittest.mock import patch, MagicMock
from ai_core.compatibility_matrix import CompatibilityMatrix


class TestCompatibilityMatrix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = CompatibilityMatrix()

    @patch("sqlite3.connect")
    def test_add_compatibility_record(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        result = self.matrix.add_compatibility_record(
            "numpy", "1.21.0", "3.8", "compatible"
        )
        self.assertTrue(result)
        mock_conn.execute.assert_called_once()

    @patch("sqlite3.connect")
    def test_check_compatibility(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("compatible",)

        result = self.matrix.check_compatibility("numpy", "1.21.0", "3.8")
        self.assertEqual(result, "compatible")

    @patch("sqlite3.connect")
    def test_find_compatible_versions(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("1.21.0",), ("1.20.0",)]

        result = self.matrix.find_compatible_versions("numpy", "3.8")
        self.assertEqual(result, ["1.21.0", "1.20.0"])


if __name__ == "__main__":
    unittest.main()
