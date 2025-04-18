"""
MechanicalMind Logging Configuration v2.0
Centralized logging setup for all modules
"""

import logging
from pathlib import Path
import sys
from typing import Optional


def configure_logging(
    log_file: Optional[str or Path] = None, level: str = "INFO"
) -> logging.Logger:
    """Configure consistent logging for all modules"""

    log_level = getattr(logging, level.upper(), logging.INFO)

    logger = logging.getLogger("mechmind")
    logger.setLevel(log_level)

    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    # Configure third-party loggers
    for lib in ["urllib3", "git", "requests"]:
        logging.getLogger(lib).setLevel(logging.WARNING)

    return logger


def get_module_logger(module_name: str) -> logging.Logger:
    """Get pre-configured logger for a module"""
    return logging.getLogger(f"mechmind.{module_name}")
