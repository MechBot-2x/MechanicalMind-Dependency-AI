"""Modelos de datos compartidos por el core de MechMind AI."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class Package:
    """Un paquete detectado en un manifiesto."""

    name: str
    version: str = ""
    ecosystem: str = ""
    source: str = ""


@dataclass
class ScanResult:
    """Resultado de un escaneo de proyecto."""

    path: str
    ecosystems: list[str] = field(default_factory=list)
    packages: list[Package] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    summary: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "ecosystems": self.ecosystems,
            "packages": [asdict(p) for p in self.packages],
            "warnings": self.warnings,
            "summary": self.summary,
        }
