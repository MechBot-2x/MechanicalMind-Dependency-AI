"""
MechanicalMind Utilities Package v2.0
Utility functions for the Dependency AI system
"""

from .file_helpers import (
    handle_file_errors,
    safe_read_file,
    atomic_write_file,
    read_json_file,
    write_json_file,
    read_yaml_file,
    write_yaml_file,
    file_checksum,
    find_files_by_pattern,
)
from .logging_config import setup_logging
from .network_helpers import fetch_url

__all__ = [
    "handle_file_errors",
    "safe_read_file",
    "atomic_write_file",
    "read_json_file",
    "write_json_file",
    "read_yaml_file",
    "write_yaml_file",
    "file_checksum",
    "find_files_by_pattern",
    "setup_logging",
    "fetch_url",
]

from .network_helpers import (
    check_internet_connection,
    download_file,
    get_pypi_package_info,
    is_port_available,
)
from .logging_config import configure_logging, get_module_logger

__all__ = [name for name in globals() if not name.startswith("_")]
