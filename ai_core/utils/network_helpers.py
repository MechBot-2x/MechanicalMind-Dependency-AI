import requests
from typing import Optional, Dict, Any
from urllib.parse import urlparse


def fetch_url(url: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
    """Fetch data from a URL with error handling"""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def check_internet_connection(test_url: str = "https://www.google.com") -> bool:
    """Check if internet connection is available"""
    try:
        requests.get(test_url, timeout=5)
        return True
    except:
        return False


def download_file(url: str, save_path: str) -> bool:
    """Download a file from URL to local path"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False


def get_pypi_package_info(package_name: str) -> Optional[Dict[str, Any]]:
    """Get package info from PyPI"""
    return fetch_url(f"https://pypi.org/pypi/{package_name}/json")


def is_port_available(host: str, port: int) -> bool:
    """Check if a network port is available"""
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) != 0
