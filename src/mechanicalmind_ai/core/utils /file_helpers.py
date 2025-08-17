from pathlib import Path
import yaml
import json
import hashlib

def safe_read_file(file_path: str or Path, encoding: str = 'utf-8') -> str:
    """Read file with error handling"""
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            return f.read()
    except Exception as e:
        raise IOError(f"Failed to read {file_path}: {str(e)}")

def read_yaml(file_path: str or Path) -> dict:
    """Safely read YAML file"""
    content = safe_read_file(file_path)
    try:
        return yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {file_path}: {str(e)}")

def write_json(data: dict, file_path: str or Path, indent: int = 2) -> bool:
    """Write data to JSON file"""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=indent)
        return True
    except Exception as e:
        raise IOError(f"Failed to write JSON to {file_path}: {str(e)}")

def file_checksum(file_path: str or Path, algorithm: str = 'sha256') -> str:
    """Calculate file checksum"""
    hash_func = getattr(hashlib, algorithm)()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def find_files_by_pattern(directory: str or Path, pattern: str) -> list:
    """Find files matching pattern recursively"""
    path = Path(directory)
    return [str(p) for p in path.rglob(pattern) if p.is_file()]
