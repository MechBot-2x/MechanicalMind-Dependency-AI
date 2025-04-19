import pytest
from ai_core.utils import __version__, __author__


def test_version():
    assert __version__ == "3.0.1"


def test_author():
    assert "MechMind Team" in __author__
    assert "dev@mechmind.example" in __author__


def test_imports():
    from ai_core.utils import configure_logging, make_http_request

    assert callable(configure_logging)
    assert callable(make_http_request)
