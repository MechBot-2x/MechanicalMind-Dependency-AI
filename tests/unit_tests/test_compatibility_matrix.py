import unittest
from unittest.mock import patch, MagicMock
from ai_core.compatibility_matrix import CompatibilityMatrix


class TestCompatibilityMatrix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = CompatibilityMatrix()
        cls.test_db_data = {
            "package_versions": [
                ("numpy", "1.21.0", "3.8", "compatible"),
                ("pandas", "1.3.0", "3.8", "compatible"),
            ],
            "package_relations": [("numpy", "1.21.0", "pandas", ">=1.3.0", "depends")],
        }

    def mock_db_connection(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        return mock_conn, mock_cursor

    @patch("sqlite3.connect")
    def test_add_compatibility_record(self, mock_connect):
        mock_conn, mock_cursor = self.mock_db_connection(mock_connect)

        result = self.matrix.add_compatibility_record(
            "numpy", "1.21.0", "3.8", "compatible"
        )
        self.assertTrue(result)
        mock_conn.execute.assert_called_once()

    @patch("sqlite3.connect")
    def test_check_compatibility(self, mock_connect):
        mock_conn, mock_cursor = self.mock_db_connection(mock_connect)
        mock_cursor.fetchone.return_value = ("compatible",)

        result = self.matrix.check_compatibility("numpy", "1.21.0", "3.8")
        self.assertEqual(result, "compatible")
        mock_cursor.execute.assert_called_once()

    @patch("sqlite3.connect")
    def test_find_compatible_versions(self, mock_connect):
        mock_conn, mock_cursor = self.mock_db_connection(mock_connect)
        mock_cursor.fetchall.return_value = [("1.21.0",), ("1.20.0",)]

        result = self.matrix.find_compatible_versions("numpy", "3.8")
        self.assertEqual(result, ["1.21.0", "1.20.0"])

    @patch("sqlite3.connect")
    def test_get_dependencies(self, mock_connect):
        mock_conn, mock_cursor = self.mock_db_connection(mock_connect)
        mock_cursor.fetchall.return_value = [("pandas", ">=1.3.0", "depends")]

        result = self.matrix.get_dependencies("numpy", "1.21.0")
        self.assertEqual(result, [("pandas", ">=1.3.0", "depends")])


if __name__ == "__main__":
    unittest.main()
