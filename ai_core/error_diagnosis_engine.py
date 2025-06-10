"""
MechanicalMind Error Diagnosis Engine v3.0
Core module for error analysis and resolution
"""

import re
import logging
from typing import Dict, List
import json
from pathlib import Path

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class ErrorDiagnosisEngine:
    def __init__(self, knowledge_base_path: str = None):
        self.logger = logging.getLogger("MechMind.Diagnosis")
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        self.error_patterns = {
            "DEPENDENCY_SYNTAX_ERROR": [
                r"dependency_file_not_evaluatable",
                r"Invalid requirement:",
                r"Parse error in requirements file",
            ],
            "GIT_CONFIG_ERROR": [
                r"git@github\.com",
                r"Permission denied \(publickey\)",
                r"Could not read from remote repository",
            ],
            "PYTHON_EXECUTION_FAILURE": [
                r"exit 1",
                r"ModuleNotFoundError",
                r"ImportError",
            ],
        }

    def _load_knowledge_base(self, path: str = None) -> Dict:
        """Carga la base de conocimiento con manejo de errores"""
        default_path = Path(__file__).parent / "knowledge_base" / "common_errors.json"
        kb_path = Path(path) if path else default_path

        try:
            with open(kb_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load knowledge base: {e}")
            return {}

    def classify_error(self, log_text: str) -> str:
        """Clasificación de errores con logging"""
        if not log_text:
            return "EMPTY_ERROR"

        log_text = log_text.lower()
        for error_type, patterns in self.error_patterns.items():
            for pattern in patterns:
                try:
                    if re.search(pattern, log_text, re.IGNORECASE):
                        self.logger.info(f"Matched error type: {error_type}")
                        return error_type
                except re.error as e:
                    self.logger.warning(f"Invalid regex pattern: {pattern} - {e}")
        return "UNKNOWN_ERROR"

    def get_solutions(self, error_type: str) -> List[str]:
        """Obtiene soluciones con fallback seguro"""
        return self.knowledge_base.get(error_type, {}).get(
            "solutions", ["Check system documentation", "Contact support team"]
        )

    def full_diagnosis(self, error_log: str) -> Dict:
        """Diagnóstico completo con metadatos"""
        error_type = self.classify_error(error_log)
        return {
            "error_type": error_type,
            "solutions": self.get_solutions(error_type),
            "confidence": 0.9 if error_type != "UNKNOWN_ERROR" else 0.3,
            "timestamp": datetime.datetime.now().isoformat(),
        }


if __name__ == "__main__":
    engine = ErrorDiagnosisEngine()
    test_error = "ERROR: dependency_file_not_evaluatable in requirements.txt"
    print(engine.classify_error(test_error))
