"""
ProjectScanner - Escaneo multi-ecosystem para MechMind AI V3.

Delega el parsing en el registro de plugins (core.plugins.registry).
"""

from __future__ import annotations

from pathlib import Path

from .models import Package, ScanResult  # reexportados por compatibilidad
from .plugins import registry

# Carpetas que nunca escaneamos
EXCLUDE_DIRS = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        "venv",
        ".venv",
        "mechmind-env",
        "env",
        "node_modules",
        "build",
        "dist",
        "__pycache__",
        ".tox",
        ".nox",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    }
)


class ProjectScanner:
    """Escanea un directorio usando los parsers registrados."""

    def __init__(self, path: str | Path = "."):
        self.path = Path(path).resolve()

    def _iter_matches(self, pattern: str):
        """Itera archivos que matchean `pattern`, saltando EXCLUDE_DIRS."""
        for p in self.path.rglob(pattern):
            if any(part in EXCLUDE_DIRS for part in p.parts):
                continue
            if p.is_file():
                yield p

    def scan(self) -> ScanResult:
        if not self.path.exists():
            return ScanResult(
                path=str(self.path),
                warnings=[f"La ruta no existe: {self.path}"],
                summary={"total_packages": 0, "total_files": 0, "ecosystems": []},
            )

        result = ScanResult(path=str(self.path))
        ecosystems: set[str] = set()
        seen_paths: set[Path] = set()
        files_scanned = 0

        for parser in registry.list():
            for pattern in parser.filename_patterns:
                for p in self._iter_matches(pattern):
                    if p in seen_paths:
                        continue
                    seen_paths.add(p)
                    files_scanned += 1
                    try:
                        pkgs = parser.parse(p)
                        result.packages.extend(pkgs)
                        ecosystems.update(pkg.ecosystem for pkg in pkgs)
                    except Exception as e:
                        result.warnings.append(f"{p}: {e}")

        result.ecosystems = sorted(ecosystems)
        result.summary = {
            "total_packages": len(result.packages),
            "total_files": files_scanned,
            "ecosystems": result.ecosystems,
        }
        return result
