# tests/unit_tests/test_utils_init.py
import unittest
from ai_core.utils import __version__, __author__


class TestUtilsInit(unittest.TestCase):
    def test_version_info(self):
        self.assertTrue(isinstance(__version__, str))
        self.assertTrue(isinstance(__author__, str))


if __name__ == "__main__":
    unittest.main()
