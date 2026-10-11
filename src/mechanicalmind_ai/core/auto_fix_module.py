"""
MechanicalMind Auto-Fix Module v3.0
Resolución automática de conflictos de dependencias.

Regla: cada `_fix_*` debe:
  1. Leer el contexto con context.get("clave", default) — nunca context["clave"].
  2. Devolver siempre un dict con {"success": bool, ...}.
  3. No asumir red, archivo, permiso ni versión disponible.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Dict, List


class DependencyAutoFixer:
    """Auto-fixer de conflictos de dependencias."""

    def __init__(self, virtualenv_path: str | None = None):
        self.virtualenv_path = Path(virtualenv_path) if virtualenv_path else None
        self.fix_strategies = {
            "VERSION_NOT_FOUND": self._fix_version_not_found,
            "DISTRIBUTION_NOT_AVAILABLE": self._fix_distribution_unavailable,
            "GIT_SSH_AUTH_ERROR": self._fix_git_ssh_error,
        }

    # ───────────────────────────── API pública ─────────────────────────────

    def apply_fix(self, error_type: str, context: dict) -> dict:
        """Aplica el fix adecuado. Defensivo ante excepciones internas."""
        fixer = self.fix_strategies.get(error_type, self._generic_fix)
        try:
            result = fixer(context)
        except Exception as e:
            return {
                "success": False,
                "action": "none",
                "message": f"Error aplicando fix '{error_type}': {e}",
                "context": context,
            }
        if not isinstance(result, dict):
            return {"success": False, "reason": "El fixer no devolvió un dict"}
        return result

    # ───────────────────────────── Estrategias ─────────────────────────────

    def _fix_version_not_found(self, context: dict) -> dict:
        """Maneja errores de versión no encontrada."""
        package = context.get("package") or ""
        required_version = context.get("required_version") or ""
        requirement_file = context.get("requirement_file") or ""

        available_versions = self._get_available_versions(package)
        if not available_versions:
            return {
                "success": False,
                "reason": "No versions available (¿sin red o paquete inexistente?)",
                "package": package,
            }

        compatible = self._find_compatible_version(required_version, available_versions)

        # Sin archivo destino → solo recomendar
        if not requirement_file:
            return {
                "success": True,
                "action": "recommend",
                "message": (
                    f"Instala {package}=={compatible} manualmente, "
                    f"o pasa -r requirements.txt --apply para editarlo"
                ),
                "package": package,
                "suggested_version": compatible,
            }

        # Con archivo destino → escribir
        return self._update_requirement_file(
            requirement_file, package, required_version, compatible
        )

    def _fix_distribution_unavailable(self, context: dict) -> dict:
        """Maneja errores de distribución no disponible."""
        return {
            "success": False,
            "action": "none",
            "message": "Distribución no disponible; verifica el nombre del paquete.",
            "context": context,
        }

    def _fix_git_ssh_error(self, context: dict) -> dict:
        """Maneja errores de autenticación SSH con git."""
        return {
            "success": False,
            "action": "none",
            "message": "Error SSH con git; revisa tus claves o usa HTTPS.",
            "context": context,
        }

    def _generic_fix(self, context: dict) -> dict:
        """Fallback: no hay estrategia específica."""
        return {
            "success": False,
            "action": "none",
            "message": "No hay auto-fix específico para este tipo de error.",
            "context": context,
        }

    def _create_clean_environment(self) -> dict:
        """Crea un venv limpio. Útil para arrancar de cero."""
        try:
            target = self.virtualenv_path or Path(".venv_clean")
            subprocess.run(
                [sys.executable, "-m", "venv", str(target)],
                check=True,
                capture_output=True,
                text=True,
            )
            return {"success": True, "action": "create_venv", "path": str(target)}
        except subprocess.CalledProcessError as e:
            return {"success": False, "reason": str(e)}

    # ───────────────────────────── Helpers ─────────────────────────────────

    def _get_available_versions(self, package: str) -> list[str]:
        """Versiones disponibles en PyPI, ordenadas semánticamente."""
        if not package:
            return []
        try:
            from .utils.network_helpers import get_pypi_package_info

            info = get_pypi_package_info(package)
            if not info:
                return []
            releases = list(info.get("releases", {}).keys())
            return self._sort_versions(releases)
        except Exception:
            return []

    @staticmethod
    def _sort_versions(versions: list[str]) -> list[str]:
        """Ordena versiones con packaging.version.Version (no lexicográfico)."""
        from packaging.version import InvalidVersion, Version

        def key(v: str) -> Version:
            try:
                return Version(v)
            except InvalidVersion:
                return Version("0")

        return sorted(versions, key=key)

    def _find_compatible_version(self, required_version: str, available_versions: list[str]) -> str:
        """Encuentra la mayor versión que cumpla el requisito."""
        if not available_versions:
            return ""
        if not required_version:
            return available_versions[-1]
        try:
            from packaging.specifiers import SpecifierSet
            from packaging.version import InvalidVersion, Version

            spec = SpecifierSet(required_version)
            for v in reversed(available_versions):
                try:
                    if Version(v) in spec:
                        return v
                except InvalidVersion:
                    continue
            return available_versions[-1]
        except Exception:
            return available_versions[-1]

    def _update_requirement_file(self, path: str, package: str, old: str, new: str) -> dict:
        """Reemplaza la línea de `package` por `package==new` en el archivo."""
        p = Path(path)
        if not p.exists():
            return {"success": False, "reason": f"No existe {path}"}
        lines = p.read_text(encoding="utf-8").splitlines()
        out, changed = [], False
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                if (
                    stripped.split("=")[0].split(">")[0].split("<")[0].strip().lower()
                    == package.lower()
                ):
                    out.append(f"{package}=={new}")
                    changed = True
                    continue
            out.append(line)
        if changed:
            p.write_text("\n".join(out) + "\n", encoding="utf-8")
        return {
            "success": changed,
            "action": "update" if changed else "no_change",
            "path": str(p),
            "package": package,
            "version": new,
        }
