"""
MechanicalMind Error Diagnosis Engine v2.0
AI-powered dependency error analysis and resolution
"""

import re
import logging
from typing import Dict, List
import json
from pathlib import Path

class ErrorDiagnosisEngine:
    def __init__(self, knowledge_base_path: str = None):
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        self.logger = logging.getLogger('ErrorDiagnosis')
        
    def _load_knowledge_base(self, path: str = None) -> Dict:
        """Load error patterns and solutions"""
        default_path = Path(__file__).parent / 'knowledge_base' / 'common_errors.json'
        kb_path = Path(path) if path else default_path
        
        try:
            with open(kb_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load knowledge base: {e}")
            return {}

    def diagnose(self, log_text: str) -> Dict:
        """Main diagnosis entry point"""
        error_type = self._classify_error(log_text)
        solution = self._find_solution(error_type, log_text)
        
        return {
            "error_type": error_type,
            "solution": solution,
            "confidence": self._calculate_confidence(log_text, error_type),
            "related_errors": self._find_related_errors(error_type)
        }

    def _classify_error(self, log_text: str) -> str:
        """Classify error based on patterns"""
        log_text = log_text.lower()
        
        # Check against known patterns
        for error_type, data in self.knowledge_base.items():
            for pattern in data.get("patterns", []):
                if re.search(pattern, log_text):
                    return error_type
        
        # Heuristic matching
        if "could not find a version" in log_text:
            return "VERSION_NOT_FOUND"
        elif "no matching distribution" in log_text:
            return "DISTRIBUTION_NOT_AVAILABLE"
        elif "git@github.com" in log_text and "permission denied" in log_text:
            return "GIT_SSH_AUTH_ERROR"
        
        return "UNKNOWN_ERROR"

    def _find_solution(self, error_type: str, log_text: str) -> List[str]:
        """Find solution steps for error"""
        # First try exact matches
        if error_type in self.knowledge_base:
            return self.knowledge_base[error_type].get("solutions", [])
        
        # Fallback to generic solutions
        return [
            "Check network connectivity",
            "Verify package exists in repository",
            "Try with different version specifiers"
        ]

    # [...] (Additional diagnostic methods)