"""
MechMind AI Core.

Exporta la API pública de las clases de negocio, utilidades y plugins.
"""

# ─── Modelos ───
# ─── Clases de negocio ───
from .analyzer import DependencyAnalyzer
from .auto_fix_module import DependencyAutoFixer
from .compatibility_matrix import CompatibilityMatrix
from .error_diagnosis_engine import ErrorDiagnosisEngine
from .learn import TelemetryStore
from .models import Package, ScanResult
from .monitor import ChangeSet, DependencyMonitor

# ─── Sistema de plugins ───
from .plugins import (
    Parser,
    ParserRegistry,
    list_parsers,
    register_parser,
    registry,
    unregister_parser,
)
from .scanner import ProjectScanner

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
    # Modelos
    "Package",
    "ScanResult",
    # Clases
    "DependencyAnalyzer",
    "DependencyAutoFixer",
    "CompatibilityMatrix",
    "ErrorDiagnosisEngine",
    "TelemetryStore",
    "DependencyMonitor",
    "ChangeSet",
    "ProjectScanner",
    # Plugins
    "Parser",
    "ParserRegistry",
    "registry",
    "register_parser",
    "unregister_parser",
    "list_parsers",
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
