"""
Compatibility bridge for auto_fix_module
Redirects to src/mechanicalmind_ai/core/auto_fix_module.py implementation
"""

try:
    from mechanicalmind_ai.core.auto_fix_module import DependencyAutoFixer
except ImportError:
    # Fallback local si el paquete src no está en el path directo
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent / "src"))
    from mechanicalmind_ai.core.auto_fix_module import DependencyAutoFixer

def fix_requirement_conflict(package, current_version, suggested_version):
    """Función de compatibilidad heredada"""
    fixer = DependencyAutoFixer()
    return fixer.apply_fix("VERSION_NOT_FOUND", {
        "package": package,
        "required_version": suggested_version,
        "requirement_file": "requirements.txt"
    })

__all__ = ["DependencyAutoFixer", "fix_requirement_conflict"]
