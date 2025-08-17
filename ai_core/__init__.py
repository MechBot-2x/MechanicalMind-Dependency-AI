"""Core module for MechanicalMind AI."""
import warnings


def _suppress_warnings():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # Resto del código...


__version__ = "3.0.0"
