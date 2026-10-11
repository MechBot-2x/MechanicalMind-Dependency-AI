"""
DependencyMonitor - Vigila cambios en las dependencias de un proyecto.

Uso típico:
    monitor = DependencyMonitor(path=".")
    monitor.run_once()              # un solo chequeo
    monitor.watch(interval=10)      # loop hasta Ctrl-C
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path

from .scanner import Package, ProjectScanner


@dataclass
class ChangeSet:
    """Diferencias entre dos snapshots de dependencias."""

    added: list[Package] = field(default_factory=list)
    removed: list[Package] = field(default_factory=list)
    changed: list[tuple[Package, Package]] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not (self.added or self.removed or self.changed)

    def to_dict(self) -> dict:
        return {
            "added": [
                {"name": p.name, "version": p.version, "ecosystem": p.ecosystem} for p in self.added
            ],
            "removed": [
                {"name": p.name, "version": p.version, "ecosystem": p.ecosystem}
                for p in self.removed
            ],
            "changed": [
                {
                    "name": old.name,
                    "ecosystem": old.ecosystem,
                    "from": old.version,
                    "to": new.version,
                }
                for old, new in self.changed
            ],
        }


class DependencyMonitor:
    """Vigila cambios en las dependencias de un proyecto."""

    def __init__(self, path: str | Path = "."):
        self.path = Path(path).resolve()
        self._last: dict[tuple[str, str], Package] = {}

    # ────────────────────────── API pública ──────────────────────────

    def _snapshot(self) -> dict[tuple[str, str], Package]:
        """Escanea el proyecto y devuelve un dict {clave → Package}."""
        result = ProjectScanner(self.path).scan()
        snapshot: dict[tuple[str, str], Package] = {}
        for pkg in result.packages:
            # Clave por (ecosystem, name) — ignoramos la version para detectar cambios
            key = (pkg.ecosystem, pkg.name)
            snapshot[key] = pkg
        return snapshot

    def run_once(self) -> ChangeSet:
        """Ejecuta un solo chequeo y devuelve los cambios vs. el anterior."""
        current = self._snapshot()

        changes = ChangeSet()
        for key, pkg in current.items():
            if key not in self._last:
                changes.added.append(pkg)
            else:
                old = self._last[key]
                if old.version != pkg.version:
                    changes.changed.append((old, pkg))

        for key, pkg in self._last.items():
            if key not in current:
                changes.removed.append(pkg)

        self._last = current
        return changes

    def watch(self, interval: float = 10.0, on_change=None) -> None:
        """Bucle infinito que corre `run_once` cada `interval` segundos.

        `on_change(changes)` es un callback opcional que se llama solo si
        hay cambios. Sin callback, los cambios se imprimen por stdout.
        """
        # Primer escaneo para inicializar el estado
        self.run_once()

        try:
            while True:
                time.sleep(interval)
                changes = self.run_once()
                if not changes.is_empty:
                    if on_change:
                        on_change(changes)
                    else:
                        self._print_changes(changes)
        except KeyboardInterrupt:
            print("\n👋 Monitor detenido por el usuario.")
        except Exception as e:
            print(f"\n❌ Error en el monitor: {e}")

    # ────────────────────────── Helpers ──────────────────────────

    @staticmethod
    def _print_changes(changes: ChangeSet) -> None:
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{ts}] 🔔 Cambios detectados:")
        for pkg in changes.added:
            print(f"  + [{pkg.ecosystem:6}] {pkg.name} {pkg.version}")
        for pkg in changes.removed:
            print(f"  - [{pkg.ecosystem:6}] {pkg.name} {pkg.version}")
        for old, new in changes.changed:
            print(f"  ~ [{new.ecosystem:6}] {new.name} {old.version} → {new.version}")
