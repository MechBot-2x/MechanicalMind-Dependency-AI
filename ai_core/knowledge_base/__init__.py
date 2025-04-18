"""
Módulo de Base de Conocimiento - Versión Corregida
=================================================
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


def load_error_knowledge(file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Carga la base de conocimiento desde un archivo JSON.

    Args:
        file_path: Ruta opcional al archivo JSON. Por defecto usa 'common_errors.json'
                  en el directorio del módulo.

    Returns:
        Diccionario con la estructura {common_errors: {error1: details, ...}}

    Raises:
        ImportError: Si hay problemas al cargar el archivo
        ValueError: Si la estructura no es válida
    """
    try:
        # Ruta por defecto si no se especifica
        kb_path = (
            Path(file_path)
            if file_path
            else Path(__file__).parent / "common_errors.json"
        )

        with open(kb_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Validación de estructura
        if not isinstance(data, dict) or "common_errors" not in data:
            raise ValueError(
                "La estructura debe contener 'common_errors' como clave principal"
            )

        return data

    except FileNotFoundError as e:
        raise ImportError(f"Archivo no encontrado: {kb_path}") from e
    except json.JSONDecodeError as e:
        raise ImportError(f"Error decodificando JSON: {str(e)}") from e
    except Exception as e:
        raise ImportError(f"Error cargando base de conocimiento: {str(e)}") from e


# Eliminado: No más carga automática al importar
