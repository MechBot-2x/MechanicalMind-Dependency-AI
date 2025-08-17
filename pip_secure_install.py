import subprocess
import sys


def safe_install():
    # Primero instalar pip sin dependencias problemáticas
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
            "setuptools",
            "wheel",
            "--no-deps",
        ]
    )

    # Luego instalar rich desde fuente limpia
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--no-binary", ":all:", "rich==13.7.0"]
    )

    # Verificar integridad
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from rich.box import Box; print('✅ Rich instalado correctamente')",
        ],
        capture_output=True,
    )
    print(result.stdout.decode() if result.returncode == 0 else "❌ Error en rich")


if __name__ == "__main__":
    safe_install()
