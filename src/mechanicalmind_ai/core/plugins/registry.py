"""
Registro de parsers para ProjectScanner.

Permite añadir soporte a nuevos ecosistemas sin tocar el scanner.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from ..models import Package


@dataclass
class Parser:
    """Un parser de manifiesto de dependencias."""

    name: str
    ecosystem: str
    description: str
    filename_patterns: tuple[str, ...]
    parse: Callable[[Path], list[Package]]


class ParserRegistry:
    """Registro de parsers. No es singleton por diseño: se instancia 1 global."""

    def __init__(self) -> None:
        self._parsers: dict[str, Parser] = {}

    def register(self, parser: Parser, *, replace: bool = False) -> None:
        if parser.name in self._parsers and not replace:
            raise ValueError(f"Parser ya registrado: {parser.name}")
        self._parsers[parser.name] = parser

    def unregister(self, name: str) -> None:
        self._parsers.pop(name, None)

    def get(self, name: str) -> Parser | None:
        return self._parsers.get(name)

    def list(self) -> list[Parser]:
        return sorted(self._parsers.values(), key=lambda p: (p.ecosystem, p.name))

    def ecosystems(self) -> list[str]:
        return sorted({p.ecosystem for p in self._parsers.values()})

    def clear(self) -> None:
        self._parsers.clear()


# Instancia global compartida
registry = ParserRegistry()


def register_parser(parser: Parser, *, replace: bool = False) -> None:
    """Registra un parser nuevo en el registro global."""
    registry.register(parser, replace=replace)


def unregister_parser(name: str) -> None:
    """Elimina un parser del registro global."""
    registry.unregister(name)


def list_parsers() -> list[Parser]:
    """Devuelve todos los parsers registrados (ordenados)."""
    return registry.list()
