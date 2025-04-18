import unittest
from unittest.mock import patch
from ai_core.utils import __version__, __author__


class TestUtilsInit(unittest.TestCase):
    def test_version_info_exists(self):
        self.assertTrue(hasattr(__import__("ai_core.utils"), "__version__"))
        self.assertTrue(hasattr(__import__("ai_core.utils"), "__author__"))
        self.assertIsInstance(__version__, str)
        self.assertIsInstance(__author__, str)

    @patch("ai_core.utils.file_helpers")
    @patch("ai_core.utils.network_helpers")
    @patch("ai_core.utils.logging_config")
    def test_imports(self, mock_logging, mock_network, mock_file):
        # Test que todos los módulos se importan correctamente
        from ai_core.utils import (
            safe_read_file,
            check_internet_connection,
            configure_logging,
        )

        self.assertTrue(callable(safe_read_file))
        self.assertTrue(callable(check_internet_connection))
        self.assertTrue(callable(configure_logging))


if __name__ == "__main__":
    unittest.main()
