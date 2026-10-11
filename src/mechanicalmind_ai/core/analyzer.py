"""
DependencyAnalyzer - Análisis de dependencias para MechMind AI V3.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class DependencyAnalyzer:
    """Analiza requirements y resuelve dependencias de paquetes."""

    def __init__(self, requirements_file: str | Path | None = None):
        self.requirements_file = Path(requirements_file) if requirements_file else None

    def parse_requirements_txt(self, file_path: str | Path) -> list[str]:
        path = Path(file_path)
        packages: list[str] = []
        for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            packages.append(line)
        return packages

    def _get_package_dependencies(self, package: str) -> str:
        result = subprocess.run(
            ["pip", "show", package],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout

    def analyze(self, project_path: str | Path) -> dict:
        path = Path(project_path)
        return {"status": "success", "path": str(path), "exists": path.exists()}
