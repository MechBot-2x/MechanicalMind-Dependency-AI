"""
CLI de MechMind AI v3.

Comandos:
    mechmind scan      Escanea un proyecto en busca de dependencias
    mechmind diagnose  Diagnostica un error de dependencia
    mechmind fix       Intenta un auto-fix (--apply para escribir)
    mechmind verify    Verifica el checksum de un archivo
    mechmind version   Muestra la versión
    mechmind monitor   (Roadmap)
    mechmind learn     (Roadmap)
    mechmind plugins   (Roadmap)
"""

from __future__ import annotations

import json
import sys

import click

from mechanicalmind_ai import __version__


@click.group()
@click.version_option(version=__version__, prog_name="mechmind")
def cli() -> None:
    """MechMind AI — Gestión inteligente de dependencias."""


# ─────────────────────────────── scan ──────────────────────────────────────


@cli.command()
@click.option("--path", "-p", default=".", help="Directorio a escanear.")
@click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Formato de salida.",
)
def scan(path: str, output_format: str) -> None:
    """Escanea un proyecto y reporta las dependencias detectadas."""
    from mechanicalmind_ai.core import ProjectScanner

    result = ProjectScanner(path).scan()

    if output_format == "json":
        click.echo(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        return

    click.echo(f"\n🔎 Escaneando: {result.path}")
    if result.warnings:
        click.echo("\n⚠️  Warnings:")
        for w in result.warnings:
            click.echo(f"   • {w}")

    click.echo(f"\n📦 Paquetes detectados: {result.summary.get('total_packages', 0)}")
    click.echo(f"🧩 Ecosistemas: {', '.join(result.ecosystems) or '—'}")

    if not result.packages:
        click.echo("\n(Sin paquetes que mostrar)")
        return

    click.echo("\nPaquetes:")
    seen: set[tuple[str, str, str]] = set()
    for pkg in result.packages:
        key = (pkg.ecosystem, pkg.name, pkg.version)
        if key in seen:
            continue
        seen.add(key)
        ver = f" {pkg.version}" if pkg.version else ""
        click.echo(f"   [{pkg.ecosystem:6}] {pkg.name}{ver}")


# ─────────────────────────────── diagnose ──────────────────────────────────


@cli.command()
@click.argument("error_log")
def diagnose(error_log: str) -> None:
    """Analiza un ERROR_LOG y propone soluciones."""
    from mechanicalmind_ai.core import ErrorDiagnosisEngine

    try:
        engine = ErrorDiagnosisEngine()
        result = engine.full_diagnosis(error_log)

        click.echo("\n=== Diagnóstico MechMind AI ===")
        click.echo(f"📌 Error: {error_log[:100]}...")
        click.echo(f"🔍 Tipo: {result['error_type']}")
        click.echo(f"🔄 Confianza: {result['confidence'] * 100:.1f}%")
        click.echo("\n💡 Soluciones recomendadas:")
        for i, sol in enumerate(result["solutions"], 1):
            click.echo(f"  {i}. {sol}")
        click.echo(f"\n⏰ Timestamp: {result['timestamp']}")
        click.echo("=" * 40)
    except Exception as e:
        click.echo(f"❌ Error en el diagnóstico: {e}", err=True)
        sys.exit(1)


# ─────────────────────────────── fix ───────────────────────────────────────


@cli.command()
@click.option("--error-type", "-e", default="VERSION_NOT_FOUND", help="Tipo de error.")
@click.option("--package", "-p", default="", help="Paquete objetivo.")
@click.option("--version-required", "-v", default="", help="Versión requerida.")
@click.option(
    "--requirement-file",
    "-r",
    default="",
    help="requirements.txt a actualizar (requiere --apply para escribir).",
)
@click.option(
    "--apply",
    is_flag=True,
    help="Escribe cambios en el archivo (por defecto: solo simula/recomienda).",
)
def fix(
    error_type: str,
    package: str,
    version_required: str,
    requirement_file: str,
    apply: bool,
) -> None:
    """Aplica un auto-fix para un tipo de error conocido."""
    from mechanicalmind_ai.core import DependencyAutoFixer

    context = {
        "package": package,
        "required_version": version_required,
        "requirement_file": requirement_file if apply else "",
    }
    result = DependencyAutoFixer().apply_fix(error_type=error_type, context=context)

    click.echo("\n=== Auto-Fix ===")
    click.echo(f"🎯 Tipo: {error_type}")
    click.echo(f"✅ Success: {result.get('success', result.get('status', 'unknown'))}")
    if "message" in result:
        click.echo(f"📝 {result['message']}")
    if "reason" in result:
        click.echo(f"ℹ️  {result['reason']}")
    if result.get("action") == "update":
        click.echo(f"📄 Archivo actualizado: {result['path']}")
    if not apply and requirement_file:
        click.echo("ℹ️  Modo simulación (añade --apply para escribir el archivo).")


# ─────────────────────────────── verify ────────────────────────────────────


@cli.command()
@click.argument("file_path", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--algorithm",
    "-a",
    type=click.Choice(["md5", "sha1", "sha256", "sha512"]),
    default="sha256",
    help="Algoritmo de hash.",
)
def verify(file_path: str, algorithm: str) -> None:
    """Calcula el checksum de un archivo."""
    from mechanicalmind_ai.core import file_checksum

    checksum = file_checksum(file_path, algorithm=algorithm)
    click.echo(f"{algorithm}: {checksum}  {file_path}")


# ─────────────────────────────── version ───────────────────────────────────


@cli.command()
def version() -> None:
    """Muestra la versión instalada."""
    click.echo(f"mechmind {__version__}")


# ─────────────────────────────── stubs ─────────────────────────────────────


@cli.command()
@click.option("--path", "-p", default=".", help="Directorio a vigilar.")
@click.option("--interval", "-i", type=float, default=10.0, help="Segundos entre chequeos.")
@click.option("--once", is_flag=True, help="Corre un solo chequeo y sale (útil para CI).")
def monitor(path: str, interval: float, once: bool) -> None:
    """Vigila cambios en las dependencias de un proyecto."""
    from mechanicalmind_ai.core import DependencyMonitor

    mon = DependencyMonitor(path=path)

    if once:
        changes = mon.run_once()
        if changes.is_empty:
            click.echo("✅ Sin cambios en el primer escaneo.")
        else:
            click.echo("🔔 Estado inicial capturado:")
            for pkg in changes.added:
                click.echo(f"  + [{pkg.ecosystem:6}] {pkg.name} {pkg.version}")
        return

    click.echo(f"👁  Vigilando {mon.path} cada {interval}s (Ctrl-C para salir)")
    mon.watch(interval=interval)


@cli.command()
def learn() -> None:
    """(Roadmap) Entrenamiento de modelos. Aún no implementado."""
    click.echo("🚧 `learn` está en roadmap. Disponible en una futura versión.")


@cli.command()
@click.argument("name", required=False)
def plugins(name: str | None) -> None:
    """Lista los parsers registrados o muestra detalles de uno.

    Sin argumentos: lista todos los parsers con su ecosistema.
    Con NAME: muestra detalles del parser NAME.
    """
    from mechanicalmind_ai.core import list_parsers, registry

    if name:
        parser = registry.get(name)
        if parser is None:
            click.echo(f"❌ Parser no encontrado: {name}", err=True)
            sys.exit(1)
        click.echo(f"\n📦 {parser.name}")
        click.echo(f"   Ecosistema  : {parser.ecosystem}")
        click.echo(f"   Descripción : {parser.description}")
        click.echo(f"   Patrones    : {', '.join(parser.filename_patterns)}")
        return

    parsers = list_parsers()
    ecos = sorted({p.ecosystem for p in parsers})

    click.echo(f"\n🔌 Parsers registrados: {len(parsers)}")
    click.echo(f"🧩 Ecosistemas: {', '.join(ecos)}\n")

    for p in parsers:
        patterns = ", ".join(p.filename_patterns)
        click.echo(f"   [{p.ecosystem:8}] {p.name:24} {patterns}")


if __name__ == "__main__":
    cli()
