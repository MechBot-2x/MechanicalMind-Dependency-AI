"""
File System Utilities Module
---------------------------

Provides robust file operations for MechanicalMind AI Dependency System v3.1.0

Key Features:
- Safe file operations with comprehensive error handling
- Atomic write operations to prevent corruption
- Support for multiple file formats (JSON, YAML, text)
- Filesystem abstraction for cross-platform compatibility
"""

import os
import json
import yaml
import tempfile
import hashlib
from pathlib import Path
from typing import Any, Optional, Union, List
import logging
from functools import wraps

_logger = logging.getLogger(__name__)


def handle_file_errors(func):
    """Decorator to standardize file operation error handling"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            _logger.error(f"File not found: {str(e)}")
            raise
        except PermissionError as e:
            _logger.error(f"Permission denied: {str(e)}")
            raise
        except Exception as e:
            _logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            raise

    return wrapper


@handle_file_errors
def safe_read_file(
    file_path: Union[str, Path], encoding: str = "utf-8"
) -> Optional[str]:
    """
    Safely read file content with comprehensive error handling

    Args:
        file_path: Path to the file to read
        encoding: Text encoding to use (default: utf-8)

    Returns:
        File content as string or None if read fails
    """
    try:
        with open(file_path, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        _logger.warning(f"Failed to read {file_path}: {str(e)}")
        return None


@handle_file_errors
def atomic_write_file(
    file_path: Union[str, Path], content: str, encoding: str = "utf-8"
) -> bool:
    """
    Atomically write content to a file using temp file replacement

    Args:
        file_path: Destination file path
        content: Content to write
        encoding: Text encoding to use

    Returns:
        True if write succeeded, False otherwise
    """
    temp_file = None
    try:
        file_path = Path(file_path)
        with tempfile.NamedTemporaryFile(
            mode="w", encoding=encoding, dir=file_path.parent, delete=False
        ) as temp_file:
            temp_file.write(content)
            temp_path = Path(temp_file.name)

        temp_path.replace(file_path)
        return True
    except Exception as e:
        _logger.error(f"Atomic write failed for {file_path}: {str(e)}")
        if temp_file:
            try:
                Path(temp_file.name).unlink(missing_ok=True)
            except Exception:
                pass
        return False


@handle_file_errors
def read_json_file(file_path: Union[str, Path]) -> Optional[dict]:
    """
    Safely read and parse JSON file

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON data or None if failed
    """
    content = safe_read_file(file_path)
    if content is None:
        return None

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        _logger.error(f"Invalid JSON in {file_path}: {str(e)}")
        return None


@handle_file_errors
def write_json_file(file_path: Union[str, Path], data: Any, indent: int = 2) -> bool:
    """
    Safely write data to JSON file with atomic operation

    Args:
        file_path: Destination file path
        data: Data to serialize
        indent: JSON indentation level

    Returns:
        True if write succeeded
    """
    try:
        content = json.dumps(data, indent=indent)
        return atomic_write_file(file_path, content)
    except Exception as e:
        _logger.error(f"JSON serialization failed: {str(e)}")
        return False


@handle_file_errors
def read_yaml_file(file_path: Union[str, Path]) -> Optional[dict]:
    """
    Safely read and parse YAML file

    Args:
        file_path: Path to YAML file

    Returns:
        Parsed YAML data or None if failed
    """
    content = safe_read_file(file_path)
    if content is None:
        return None

    try:
        return yaml.safe_load(content)
    except yaml.YAMLError as e:
        _logger.error(f"Invalid YAML in {file_path}: {str(e)}")
        return None


@handle_file_errors
def write_yaml_file(file_path: Union[str, Path], data: Any) -> bool:
    """
    Safely write data to YAML file with atomic operation

    Args:
        file_path: Destination file path
        data: Data to serialize

    Returns:
        True if write succeeded
    """
    try:
        content = yaml.dump(data)
        return atomic_write_file(file_path, content)
    except Exception as e:
        _logger.error(f"YAML serialization failed: {str(e)}")
        return False


@handle_file_errors
def file_checksum(
    file_path: Union[str, Path], algorithm: str = "sha256"
) -> Optional[str]:
    """
    Calculate file checksum

    Args:
        file_path: Path to file
        algorithm: Hash algorithm (md5, sha1, sha256)

    Returns:
        Hex digest string or None if failed
    """
    try:
        hash_func = getattr(hashlib, algorithm)()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        _logger.error(f"Checksum failed for {file_path}: {str(e)}")
        return None


@handle_file_errors
def find_files_by_pattern(
    directory: Union[str, Path], pattern: str = "*.py"
) -> List[Path]:
    """
    Find files matching pattern in directory

    Args:
        directory: Root directory to search
        pattern: Glob pattern to match

    Returns:
        List of matching file paths
    """
    directory = Path(directory)
    if not directory.is_dir():
        _logger.warning(f"Invalid directory: {directory}")
        return []

    return list(directory.rglob(pattern))
