#!/usr/bin/env python3
import click
from mechanicalmind_ai.core import ErrorDiagnosisEngine
import datetime


@click.command()
@click.argument("error_log")
def diagnose(error_log):
    """CLI para diagnóstico de errores de dependencias"""
    try:
        engine = ErrorDiagnosisEngine()
        result = engine.full_diagnosis(error_log)

        click.echo("\n=== Diagnóstico MechMind AI ===")
        click.echo(f"📌 Error: {error_log[:100]}...")
        click.echo(f"🔍 Tipo: {result['error_type']}")
        click.echo(f"🔄 Confianza: {result['confidence']*100:.1f}%")
        click.echo("\n💡 Soluciones recomendadas:")
        for i, sol in enumerate(result["solutions"], 1):
            click.echo(f"  {i}. {sol}")
        click.echo(f"\n⏰ Timestamp: {result['timestamp']}")
        click.echo("=" * 40)
    except Exception as e:
        click.echo(f"❌ Error en el diagnóstico: {str(e)}", err=True)


if __name__ == "__main__":
    diagnose()
