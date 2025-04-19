# ai_core/utils/logging_config.py
import logging
from pathlib import Path
from typing import Optional


def setup_logging(
    log_file: str = "mechmind.log", level: int = logging.INFO
) -> logging.Logger:
    """Configura logging básico para la aplicación"""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )
    return logging.getLogger(__name__)


def configure_logging(config_path: Optional[str] = None) -> logging.Logger:
    """Configuración avanzada de logging desde archivo"""
    if config_path and Path(config_path).exists():
        try:
            with open(config_path) as f:
                import json

                config = json.load(f)
                logging.config.dictConfig(config)
        except Exception as e:
            print(f"Error loading logging config: {e}")
            return setup_logging()
    return setup_logging()


def get_module_logger(name: str) -> logging.Logger:
    """Obtiene un logger configurado para un módulo específico"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        setup_logging()
    return logger
