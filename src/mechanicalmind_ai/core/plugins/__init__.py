"""
Sistema de plugins de MechMind AI.

Expone el registro de parsers y registra automáticamente los built-in.
Para añadir un nuevo parser:

    from mechanicalmind_ai.core.plugins import Parser, register_parser
    from mechanicalmind_ai.core.models import Package

    def parse_my_format(path):
        return [Package(name="...", version="...", ecosystem="my", source=str(path))]

    register_parser(Parser(
        name="my-format",
        ecosystem="my",
        description="...",
        filename_patterns=("my.manifest",),
        parse=parse_my_format,
    ))
"""

from __future__ import annotations

from . import builtin
from .registry import (
    Parser,
    ParserRegistry,
    list_parsers,
    register_parser,
    registry,
    unregister_parser,
)

# Auto-registrar los parsers built-in (replace=True por si se recarga el módulo)
for _parser in builtin.BUILTIN_PARSERS:
    registry.register(_parser, replace=True)

__all__ = [
    "Parser",
    "ParserRegistry",
    "registry",
    "register_parser",
    "unregister_parser",
    "list_parsers",
]
