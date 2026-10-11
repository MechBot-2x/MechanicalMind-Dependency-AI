"""
MechMind AI Core.

Exporta la API pública de las clases de negocio y utilidades.
"""

# ─── Clases de negocio ───
from .analyzer import DependencyAnalyzer
from .auto_fix_module import DependencyAutoFixer
from .compatibility_matrix import CompatibilityMatrix
from .error_diagnosis_engine import ErrorDiagnosisEngine
from .scanner import Package, ProjectScanner, ScanResult

# ─── Utilidades ───
from .utils.file_helpers import (
    file_checksum,
    find_files_by_pattern,
    read_yaml,
    safe_read_file,
    write_json,
)
from .utils.logging_config import configure_logging, get_module_logger
from .utils.network_helpers import (
    check_internet_connection,
    download_file,
    get_pypi_package_info,
    is_port_available,
)

__all__ = [
    # Clases
    "DependencyAnalyzer",
    "DependencyAutoFixer",
    "CompatibilityMatrix",
    "ErrorDiagnosisEngine",
    "ProjectScanner",
    "ScanResult",
    "Package",
    # Utilidades file
    "safe_read_file",
    "read_yaml",
    "write_json",
    "file_checksum",
    "find_files_by_pattern",
    # Utilidades network
    "check_internet_connection",
    "download_file",
    "get_pypi_package_info",
    "is_port_available",
    # Utilidades logging
    "configure_logging",
    "get_module_logger",
]
