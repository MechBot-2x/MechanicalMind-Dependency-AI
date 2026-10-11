"""
TelemetryStore - Estadísticas de uso locales para MechMind AI.

Todo queda en ~/.mechmind/stats.json. Nada sale a la red.

Variables de entorno:
    MECHMIND_TELEMETRY_PATH  → ruta alternativa del JSON (útil en tests)
    MECHMIND_NO_TELEMETRY=1  → desactiva la telemetría por completo
"""

from __future__ import annotations

import csv
import io
import json
import os
import time
from pathlib import Path

STATS_VERSION = 1
MAX_RECENT_EVENTS = 50


def _default_path() -> Path:
    env = os.environ.get("MECHMIND_TELEMETRY_PATH")
    if env:
        return Path(env)
    return Path.home() / ".mechmind" / "stats.json"


def _disabled() -> bool:
    return os.environ.get("MECHMIND_NO_TELEMETRY") == "1"


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def _empty() -> dict:
    now = _now()
    return {
        "version": STATS_VERSION,
        "created_at": now,
        "updated_at": now,
        "counters": {},
        "ecosystems_seen": [],
        "packages_seen": {},
        "recent_events": [],
    }


class TelemetryStore:
    """Almacén de estadísticas de uso locales."""

    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path else _default_path()
        self.enabled = not _disabled()

    # ────────────────────────── I/O ──────────────────────────

    def load(self) -> dict:
        if not self.path.exists():
            return _empty()
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if data.get("version") != STATS_VERSION:
                return _empty()
            return data
        except Exception:
            return _empty()

    def save(self, data: dict) -> None:
        if not self.enabled:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data["updated_at"] = _now()
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(self.path)

    # ────────────────────────── API pública ──────────────────────────

    def record(self, event: str, **payload) -> None:
        """Registra un evento. Nunca lanza excepción por diseño."""
        if not self.enabled:
            return
        data = self.load()
        data["counters"][event] = data["counters"].get(event, 0) + 1

        eco = payload.get("ecosystems")
        if eco:
            merged = set(data.get("ecosystems_seen", [])) | set(eco)
            data["ecosystems_seen"] = sorted(merged)

        pkgs = payload.get("packages")
        if pkgs:
            seen = data.setdefault("packages_seen", {})
            for entry in pkgs:
                if isinstance(entry, dict):
                    name, peco = entry.get("name"), entry.get("ecosystem")
                else:
                    name, peco = entry[0], entry[1]
                if not name or not peco:
                    continue
                seen.setdefault(peco, {})
                seen[peco][name] = seen[peco].get(name, 0) + 1

        event_log = {k: v for k, v in payload.items() if k != "packages"}
        event_log["ts"] = _now()
        event_log["event"] = event
        data.setdefault("recent_events", []).insert(0, event_log)
        data["recent_events"] = data["recent_events"][:MAX_RECENT_EVENTS]

        self.save(data)

    def get_stats(self) -> dict:
        return self.load()

    def reset(self) -> None:
        if self.path.exists():
            self.path.unlink()

    def export(self, fmt: str = "json") -> str:
        data = self.load()
        if fmt == "json":
            return json.dumps(data, indent=2, ensure_ascii=False)
        if fmt == "csv":
            buf = io.StringIO()
            w = csv.writer(buf)
            w.writerow(["section", "key", "value"])
            for k, v in sorted(data["counters"].items()):
                w.writerow(["counter", k, v])
            w.writerow(["meta", "created_at", data["created_at"]])
            w.writerow(["meta", "updated_at", data["updated_at"]])
            for eco in data.get("ecosystems_seen", []):
                w.writerow(["ecosystem", eco, ""])
            for eco, pkgs in data.get("packages_seen", {}).items():
                for name, count in sorted(pkgs.items()):
                    w.writerow(["package", f"{eco}:{name}", count])
            return buf.getvalue()
        raise ValueError(f"Formato no soportado: {fmt}")
