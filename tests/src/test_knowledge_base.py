# tests/unit_tests/test_knowledge_base.py
import unittest
import json
from pathlib import Path
from unittest.mock import mock_open, patch
from ai_core.knowledge_base import load_error_knowledge


class TestKnowledgeBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data = {
            "common_errors": {"ImportError": ["Missing dependency", "Incorrect path"]}
        }

    def test_load_error_knowledge(self):
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(self.test_data))
        ) as mock_file:
            with patch("pathlib.Path.exists", return_value=True):
                result = load_error_knowledge()
                self.assertIn("ImportError", result["common_errors"])

    def test_load_nonexistent_file(self):
        with patch("pathlib.Path.exists", return_value=False):
            with self.assertRaises(ImportError):
                load_error_knowledge()


if __name__ == "__main__":
    unittest.main()
