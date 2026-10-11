"""
MechanicalMind Knowledge Base Package v3.0
Initialization for knowledge base modules
"""

import json
from pathlib import Path


def load_error_knowledge() -> dict:
    """Load error knowledge base from JSON"""
    kb_path = Path(__file__).parent / "common_errors.json"
    try:
        with open(kb_path) as f:
            return json.load(f)
    except Exception as e:
        raise ImportError(f"Failed to load knowledge base: {str(e)}") from e


# Initialize on package import
error_knowledge = load_error_knowledge()
