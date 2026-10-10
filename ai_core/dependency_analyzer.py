"""
Módulo principal de análisis de dependencias - Versión Unificada V3 Advanced
Integra capacidades evolutivas y retrocompatibilidad total.
"""
from pathlib import Path
import subprocess
import logging

logger = logging.getLogger(__name__)

class DependencyAnalyzer:
    def __init__(self):
        self.dependencies = []
        
    def get_dependency_tree(self):
        """Genera y retorna el árbol de dependencias completo (Evolución V3)"""
        return {
            "status": "success",
            "dependencies": self.dependencies,
            "total_count": len(self.dependencies)
        }
    
    def analyze(self, path):
        """Método principal de análisis con detección automática de entorno"""
        resolved_path = Path(path)
        print(f"Analizando dependencias en: {resolved_path}")
        
        # Auto-detectar y parsear requirements.txt si la ruta es un directorio válido
        if resolved_path.is_dir():
            req_file = resolved_path / "requirements.txt"
            if req_file.exists():
                self.dependencies = self.parse_requirements_txt(req_file)
        elif resolved_path.is_file():
            self.dependencies = self.parse_requirements_txt(resolved_path)
            
        return {
            "status": "success",
            "path": str(resolved_path),
            "dependencies_count": len(self.dependencies),
            "dependencies": self.dependencies
        }

    def _get_package_dependencies(self, package_name):
        """Obtiene dependencias detalladas de un paquete usando pip"""
        try:
            result = subprocess.run(
                ['pip', 'show', package_name],
                capture_output=True, 
                text=True,
                check=False
            )
            if result.returncode == 0:
                return result.stdout
            return f"Error: Paquete '{package_name}' no encontrado o inactivo."
        except Exception as e:
            return f"Error obteniendo dependencias: {str(e)}"

    def parse_requirements_txt(self, file_path):
        """Parsea archivos requirements.txt filtrando comentarios y líneas vacías"""
        try:
            path = Path(file_path)
            if not path.exists():
                return []
            with open(path, 'r', encoding='utf-8') as f:
                return [
                    line.strip() 
                    for line in f 
                    if line.strip() and not line.strip().startswith('#')
                ]
        except Exception as e:
            print(f"Error leyendo archivo: {str(e)}")
            return []

def main():
    import argparse
    parser = argparse.ArgumentParser(description="MechanicalMind Dependency Analyzer - V3")
    parser.add_argument("--path", required=True, help="Ruta del proyecto o archivo a analizar")
    args = parser.parse_args()

    analyzer = DependencyAnalyzer()
    result = analyzer.analyze(args.path)
    print(result)

if __name__ == "__main__":
    main()
