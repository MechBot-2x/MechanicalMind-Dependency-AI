"""
MechanicalMind Network Utilities v2.0
Helper functions for network operations
"""

import requests
import urllib3
from typing import Optional
from pathlib import Path
import socket


def check_internet_connection(timeout: float = 3.0) -> bool:
    """Check if internet connection is available"""
    try:
        requests.get("https://pypi.org/simple/", timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


def download_file(url: str, destination: str or Path, timeout: float = 30.0) -> bool:
    """Download file from URL with progress and retries"""
    try:
        with requests.get(url, stream=True, timeout=timeout) as r:
            r.raise_for_status()
            with open(destination, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except Exception as e:
        raise IOError(f"Download failed: {str(e)}")


def get_pypi_package_info(package_name: str) -> Optional[dict]:
    """Fetch package metadata from PyPI"""
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url, timeout=10.0)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return None
        raise
    except Exception as e:
        raise ConnectionError(f"PyPI API error: {str(e)}")


def is_port_available(port: int, host: str = "localhost") -> bool:
    """Check if network port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except socket.error:
            return False
