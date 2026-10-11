"""
ProjectScanner - Escaneo multi-ecosystem para MechMind AI V3.

Detecta requirements.txt, package.json, pom.xml, pyproject.toml y Dockerfile
en un directorio y devuelve un resumen estructurado.
"""

from __future__ import annotations

import json
import re
import tomllib
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from pathlib import Path

# ─── Estructuras ───


@dataclass
class Package:
    name: str
    version: str = ""
    ecosystem: str = ""
    source: str = ""  # archivo donde se encontró


@dataclass
class ScanResult:
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


# ─── Parsers ───


def _strip_comment(line: str) -> str:
    """Elimina comentarios inline (#...) respetando comillas simples/dobles."""
    in_s = False
    in_d = False
    for i, ch in enumerate(line):
        if ch == "'" and not in_d:
            in_s = not in_s
        elif ch == '"' and not in_s:
            in_d = not in_d
        elif ch == "#" and not in_s and not in_d:
            return line[:i]
    return line


_REQ_LINE = re.compile(r"^\s*([A-Za-z0-9_.\-]+)\s*([<>=!~].*)?$")


def _parse_requirements(path: Path) -> list[Package]:
    pkgs: list[Package] = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = _strip_comment(raw).strip()
        if not line or line.startswith("#"):
            continue
        # Ignorar flags tipo -r, -e, --hash
        if line.startswith("-"):
            continue
        m = _REQ_LINE.match(line)
        if not m:
            continue
        name, ver = m.group(1), (m.group(2) or "").strip()
        pkgs.append(Package(name=name, version=ver, ecosystem="python", source=str(path)))
    return pkgs


def _parse_pyproject(path: Path) -> list[Package]:
    pkgs: list[Package] = []
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return pkgs

    project = data.get("project", {})
    for dep in project.get("dependencies", []) or []:
        m = _REQ_LINE.match(dep.strip())
        if m:
            pkgs.append(
                Package(
                    name=m.group(1),
                    version=(m.group(2) or "").strip(),
                    ecosystem="python",
                    source=str(path),
                )
            )
    return pkgs


def _parse_package_json(path: Path) -> list[Package]:
    pkgs: list[Package] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return pkgs

    for section in ("dependencies", "devDependencies", "peerDependencies"):
        for name, ver in (data.get(section) or {}).items():
            pkgs.append(Package(name=name, version=ver, ecosystem="node", source=str(path)))
    return pkgs


def _parse_pom(path: Path) -> list[Package]:
    pkgs: list[Package] = []
    try:
        tree = ET.parse(path)
    except Exception:
        return pkgs

    ns = {"m": "http://maven.apache.org/POM/4.0.0"}
    for dep in tree.getroot().findall(".//m:dependency", ns):
        g = dep.findtext("m:groupId", default="", namespaces=ns)
        a = dep.findtext("m:artifactId", default="", namespaces=ns)
        v = dep.findtext("m:version", default="", namespaces=ns)
        if a:
            pkgs.append(Package(name=f"{g}:{a}", version=v, ecosystem="java", source=str(path)))
    return pkgs


_DOCKER_FROM = re.compile(r"^\s*FROM\s+([^\s]+)", re.IGNORECASE)


def _parse_dockerfile(path: Path) -> list[Package]:
    pkgs: list[Package] = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = _DOCKER_FROM.match(raw)
        if m:
            image = m.group(1)
            if ":" in image:
                name, ver = image.rsplit(":", 1)
            else:
                name, ver = image, ""
            pkgs.append(Package(name=name, version=ver, ecosystem="docker", source=str(path)))
    return pkgs


# ─── Scanner principal ───


class ProjectScanner:
    """Escanea un directorio en busca de manifiestos de dependencias."""

    KNOWN_FILES = {
        "package.json": _parse_package_json,
        "pom.xml": _parse_pom,
        "pyproject.toml": _parse_pyproject,
        "Dockerfile": _parse_dockerfile,
    }

    def __init__(self, path: str | Path = "."):
        self.path = Path(path).resolve()

    def _find_files(self) -> dict[str, list[Path]]:
        found: dict[str, list[Path]] = {}
        # requirements*.txt (múltiples)
        reqs = list(self.path.glob("requirements*.txt"))
        if reqs:
            found["requirements.txt"] = reqs
        for name in self.KNOWN_FILES:
            matches = list(self.path.rglob(name))
            if matches:
                found[name] = matches
        return found

    def scan(self) -> ScanResult:
        if not self.path.exists():
            return ScanResult(
                path=str(self.path),
                warnings=[f"La ruta no existe: {self.path}"],
                summary={"total_packages": 0, "total_files": 0},
            )

        result = ScanResult(path=str(self.path))
        files = self._find_files()
        ecosystems: set[str] = set()

        for name, paths in files.items():
            for p in paths:
                try:
                    if name == "requirements.txt":
                        pkgs = _parse_requirements(p)
                    else:
                        pkgs = self.KNOWN_FILES[name](p)
                    result.packages.extend(pkgs)
                    ecosystems.update(pkg.ecosystem for pkg in pkgs)
                except Exception as e:
                    result.warnings.append(f"{p}: {e}")

        result.ecosystems = sorted(ecosystems)
        result.summary = {
            "total_packages": len(result.packages),
            "total_files": sum(len(v) for v in files.values()),
            "ecosystems": result.ecosystems,
        }
        return result
