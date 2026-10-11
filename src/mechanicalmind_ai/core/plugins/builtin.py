"""Parsers built-in para los ecosistemas soportados por MechMind AI."""

from __future__ import annotations

import json
import re
import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path

from ..models import Package
from .registry import Parser

# ═════════════════════════════ helpers ═════════════════════════════════


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


def _strip_slash_comment(line: str) -> str:
    """Elimina comentarios // (para go.mod)."""
    idx = line.find("//")
    return line[:idx] if idx >= 0 else line


_REQ_LINE = re.compile(r"^\s*([A-Za-z0-9_.\-]+)\s*([<>=!~].*)?$")


# ══════════════════════════════ Python ═════════════════════════════════


def _parse_requirements(path: Path) -> list[Package]:
    pkgs: list[Package] = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = _strip_comment(raw).strip()
        if not line or line.startswith("#") or line.startswith("-"):
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


# ══════════════════════════════ Node.js ════════════════════════════════


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


# ══════════════════════════════ Java ═══════════════════════════════════


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


# ══════════════════════════════ Docker ═════════════════════════════════


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


# ══════════════════════════════ Go ═════════════════════════════════════


_GO_REQUIRE_LINE = re.compile(r"^\s*([\w./\-]+)\s+(v[\w.\-+]+)\s*$")


def _parse_go_mod(path: Path) -> list[Package]:
    pkgs: list[Package] = []
    in_require = False
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = _strip_slash_comment(raw).strip()
        if not line:
            continue
        if line.startswith("require ("):
            in_require = True
            continue
        if in_require and line == ")":
            in_require = False
            continue
        target = None
        if in_require:
            target = line
        elif line.startswith("require "):
            target = line[len("require ") :].strip()
        if target:
            m = _GO_REQUIRE_LINE.match(target)
            if m:
                pkgs.append(
                    Package(
                        name=m.group(1),
                        version=m.group(2),
                        ecosystem="go",
                        source=str(path),
                    )
                )
    return pkgs


# ══════════════════════════════ Rust ═══════════════════════════════════


def _parse_cargo_toml(path: Path) -> list[Package]:
    pkgs: list[Package] = []
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return pkgs
    for section in ("dependencies", "dev-dependencies", "build-dependencies"):
        for name, spec in (data.get(section) or {}).items():
            if isinstance(spec, str):
                ver = spec
            elif isinstance(spec, dict):
                ver = spec.get("version", "")
            else:
                ver = ""
            pkgs.append(Package(name=name, version=ver, ecosystem="rust", source=str(path)))
    return pkgs


# ══════════════════════════════ Ruby ═══════════════════════════════════


_GEM_RE = re.compile(r"""^\s*gem\s+['"]([^'"]+)['"](?:\s*,\s*['"]([^'"]+)['"])?""")


def _parse_gemfile(path: Path) -> list[Package]:
    pkgs: list[Package] = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = _GEM_RE.match(line)
        if m:
            pkgs.append(
                Package(
                    name=m.group(1),
                    version=m.group(2) or "",
                    ecosystem="ruby",
                    source=str(path),
                )
            )
    return pkgs


# ══════════════════════════════ PHP ════════════════════════════════════


def _parse_composer_json(path: Path) -> list[Package]:
    pkgs: list[Package] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return pkgs
    for section in ("require", "require-dev"):
        for name, ver in (data.get(section) or {}).items():
            pkgs.append(Package(name=name, version=ver, ecosystem="php", source=str(path)))
    return pkgs


# ══════════════════════════════ Swift ══════════════════════════════════


# Captura: .package(url: "...github.com/OWNER/REPO(.git)?", from: "VERSION")
_SWIFT_PKG_RE = re.compile(
    r"\.package\s*\([^)]*?url:\s*\"[^\"]*?/([^/\"]+?)(?:\.git)?\""
    r"[^)]*?(?:from|exact|upToNextMajor|upToNextMinor)?\s*:?\s*\"([^\"]+)\""
)


def _parse_swift_package(path: Path) -> list[Package]:
    pkgs: list[Package] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for m in _SWIFT_PKG_RE.finditer(text):
        pkgs.append(
            Package(
                name=m.group(1),
                version=m.group(2),
                ecosystem="swift",
                source=str(path),
            )
        )
    return pkgs


# ══════════════════════════ Registro builtin ══════════════════════════


BUILTIN_PARSERS: list[Parser] = [
    Parser(
        name="python-requirements",
        ecosystem="python",
        description="requirements*.txt (pip)",
        filename_patterns=("requirements*.txt",),
        parse=_parse_requirements,
    ),
    Parser(
        name="python-pyproject",
        ecosystem="python",
        description="pyproject.toml [project.dependencies]",
        filename_patterns=("pyproject.toml",),
        parse=_parse_pyproject,
    ),
    Parser(
        name="node-package-json",
        ecosystem="node",
        description="package.json (npm)",
        filename_patterns=("package.json",),
        parse=_parse_package_json,
    ),
    Parser(
        name="java-maven",
        ecosystem="java",
        description="pom.xml (Maven)",
        filename_patterns=("pom.xml",),
        parse=_parse_pom,
    ),
    Parser(
        name="docker-dockerfile",
        ecosystem="docker",
        description="Dockerfile (imágenes base)",
        filename_patterns=("Dockerfile", "Dockerfile.*"),
        parse=_parse_dockerfile,
    ),
    Parser(
        name="go-mod",
        ecosystem="go",
        description="go.mod (Go modules)",
        filename_patterns=("go.mod",),
        parse=_parse_go_mod,
    ),
    Parser(
        name="rust-cargo",
        ecosystem="rust",
        description="Cargo.toml (Cargo)",
        filename_patterns=("Cargo.toml",),
        parse=_parse_cargo_toml,
    ),
    Parser(
        name="ruby-gemfile",
        ecosystem="ruby",
        description="Gemfile (Bundler)",
        filename_patterns=("Gemfile",),
        parse=_parse_gemfile,
    ),
    Parser(
        name="php-composer",
        ecosystem="php",
        description="composer.json (Composer)",
        filename_patterns=("composer.json",),
        parse=_parse_composer_json,
    ),
    Parser(
        name="swift-package",
        ecosystem="swift",
        description="Package.swift (SwiftPM)",
        filename_patterns=("Package.swift",),
        parse=_parse_swift_package,
    ),
]
