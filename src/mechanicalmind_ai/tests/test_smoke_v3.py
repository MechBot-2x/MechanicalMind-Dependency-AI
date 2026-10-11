"""Smoke test V3: verifica que el paquete V3 y sus clases importan."""

import unittest


class TestSmokeV3(unittest.TestCase):

    def test_import_engine(self):
        from mechanicalmind_ai.core import ErrorDiagnosisEngine

        self.assertTrue(callable(ErrorDiagnosisEngine))

    def test_engine_instantiable(self):
        from mechanicalmind_ai.core import ErrorDiagnosisEngine

        engine = ErrorDiagnosisEngine()
        self.assertIsNotNone(engine)

    def test_core_exports(self):
        import mechanicalmind_ai.core as core

        for name in (
            "ErrorDiagnosisEngine",
            "CompatibilityMatrix",
            "safe_read_file",
            "get_pypi_package_info",
            "configure_logging",
        ):
            self.assertTrue(hasattr(core, name), f"core no exporta {name}")


if __name__ == "__main__":
    unittest.main()
