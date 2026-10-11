"""Tests de ErrorDiagnosisEngine (V3)."""

import unittest

from mechanicalmind_ai.core.error_diagnosis_engine import ErrorDiagnosisEngine


class TestErrorDiagnosisEngine(unittest.TestCase):

    def setUp(self):
        self.engine = ErrorDiagnosisEngine()

    def test_instantiable(self):
        self.assertIsNotNone(self.engine)

    def test_classify_error_returns_string(self):
        log = "ModuleNotFoundError: No module named 'requests'"
        result = self.engine.classify_error(log)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_get_solutions_returns_list(self):
        solutions = self.engine.get_solutions("module_not_found")
        self.assertIsInstance(solutions, list)

    def test_full_diagnosis_returns_dict_with_keys(self):
        log = "ModuleNotFoundError: No module named 'requests'"
        result = self.engine.full_diagnosis(log)

        self.assertIsInstance(result, dict)
        for key in ("error_type", "confidence", "solutions", "timestamp"):
            self.assertIn(key, result, f"Falta la clave '{key}' en el resultado")
        self.assertIsInstance(result["solutions"], list)
        self.assertIsInstance(result["confidence"], (int, float))


if __name__ == "__main__":
    unittest.main()
