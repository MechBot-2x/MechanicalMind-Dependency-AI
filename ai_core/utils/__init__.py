"""
Módulo utils para MechanicalMind Dependency AI
"""

__version__ = "3.0.1"
__author__ = "MechMind Team <dev@mechmind.example>"


# Importaciones diferidas para evitar circular imports
def configure_logging():
    from .logging_config import configure_logging as _configure

    return _configure()


def make_http_request(*args, **kwargs):
    from .network_helpers import make_http_request as _make_request

    return _make_request(*args, **kwargs)


__all__ = ["__version__", "__author__", "configure_logging", "make_http_request"]
