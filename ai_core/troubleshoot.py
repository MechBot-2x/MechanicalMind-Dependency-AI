#!/usr/bin/env python
import subprocess
import platform


def check_system():
    print("🔍 Escaneando sistema...")
    issues = []

    # Verificar Python
    py = subprocess.run(["python", "--version"], capture_output=True, text=True)
    if "3.12" not in py.stdout:
        issues.append(f"⚠️  Python 3.12 requerido (tienes {py.stdout.strip()})")

    # Verificar Docker
    docker = subprocess.run(["docker", "--version"], capture_output=True)
    if docker.returncode != 0:
        issues.append("⚠️  Docker no está instalado")

    return issues


def apply_fixes():
    print("\n✨ Aplicando soluciones mágicas...")
    subprocess.run(["pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
    subprocess.run(["pip", "check"])
    print("\n🎉 ¡Hechizos aplicados! Intenta ejecutar tu proyecto nuevamente")


if __name__ == "__main__":
    problems = check_system()
    if problems:
        print("\n".join(problems))
        apply_fixes()
    else:
        print("✅ Sistema perfectamente configurado para la magia de MechanicalMind AI")
        print(
            subprocess.getoutput(
                "python -c \"from art import text2art; print(text2art('Ready!'))\""
            )
        )
