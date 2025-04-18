"""
MechanicalMind Knowledge Base Test Suite - Versión Mejorada y Corregida
======================================================================
"""

import json
import time
from pathlib import Path
from typing import Dict, Any
import unittest
from unittest.mock import patch, mock_open
from ai_core.knowledge_base import load_error_knowledge


class TestKnowledgeBase(unittest.TestCase):
    """Caso de prueba para el módulo de base de conocimiento"""

    @classmethod
    def setUpClass(cls) -> None:
        """Configuración inicial de datos de prueba"""
        cls.test_data_dir = Path(__file__).parent / "test_data"
        cls.test_data_dir.mkdir(exist_ok=True)

        # Archivo válido
        cls.valid_kb_path = cls.test_data_dir / "valid_knowledge.json"
        cls.valid_data: Dict[str, Any] = {
            "common_errors": {
                "TEST_ERROR": {
                    "description": "Test error",
                    "patterns": ["test pattern"],
                    "solutions": ["test solution"],
                    "severity": "low",
                }
            }
        }
        with open(cls.valid_kb_path, "w", encoding="utf-8") as f:
            json.dump(cls.valid_data, f, indent=2)

        # Archivo inválido
        cls.invalid_kb_path = cls.test_data_dir / "invalid_knowledge.json"
        with open(cls.invalid_kb_path, "w", encoding="utf-8") as f:
            f.write('{"key": "value"')  # JSON incompleto

    def test_large_file_performance(self):
        """Test de carga con archivo grande"""
        large_data = {"common_errors": {f"ERR{i}": {} for i in range(1000)}}
        with patch("builtins.open", mock_open(read_data=json.dumps(large_data))):
            start = time.time()
            result = load_error_knowledge()
            elapsed = time.time() - start
            self.assertLess(elapsed, 0.5)  # Menos de 500ms

    def test_load_valid_knowledge(self) -> None:
        """Test Case KB-101: Carga exitosa de conocimiento válido"""
        result = load_error_knowledge(str(self.valid_kb_path))
        self.assertEqual(result, self.valid_data)
        self.assertIn("TEST_ERROR", result["common_errors"])

    def test_load_invalid_json(self) -> None:
        """Test Case KB-401: Manejo de JSON inválido"""
        with self.assertRaises(ImportError):
            load_error_knowledge(str(self.invalid_kb_path))

    def test_file_not_found(self) -> None:
        """Test Case KB-201: Manejo de archivo no encontrado"""
        with self.assertRaises(ImportError):
            load_error_knowledge("non_existent_file.json")


if __name__ == "__main__":
    unittest.main(verbosity=2)
