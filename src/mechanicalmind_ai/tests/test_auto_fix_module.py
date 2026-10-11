"""Tests de DependencyAutoFixer (V3)."""

import unittest

from mechanicalmind_ai.core.auto_fix_module import DependencyAutoFixer


class TestDependencyAutoFixer(unittest.TestCase):

    def setUp(self):
        self.fixer = DependencyAutoFixer()

    def test_instantiable(self):
        self.assertIsNotNone(self.fixer)

    def test_apply_fix_returns_dict(self):
        result = self.fixer.apply_fix(
            error_type="module_not_found",
            context={"package": "requests", "version": "2.32.0"},
        )
        self.assertIsInstance(result, dict)

    def test_apply_fix_unknown_error_does_not_crash(self):
        result = self.fixer.apply_fix(
            error_type="error_que_no_existe",
            context={},
        )
        self.assertIsInstance(result, dict)


if __name__ == "__main__":
    unittest.main()
