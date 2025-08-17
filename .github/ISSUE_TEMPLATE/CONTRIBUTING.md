### Flujo para Reportar Problemas

1. Ve a la pestaña [Issues](https://github.com/MechBot-2x/MechanicalMind-Dependency-AI/issues)
2. Haz clic en "New Issue"
3. Selecciona la plantilla adecuada
4. Completa toda la información solicitada
5. Adjunta archivos relevantes (logs, screenshots)
```

## Implementación

1. Crea la estructura de directorios:
```bash
mkdir -p .github/ISSUE_TEMPLATE
```

2. Crea cada archivo de plantilla:
```bash
touch .github/ISSUE_TEMPLATE/{reporte-error,solicitud-funcionalidad,reporte-dependencias,problema-rendimiento,documentacion,ayuda-configuracion}.md
```

3. Agrega y commitea los cambios:
```bash
git add .github/
git commit -m "Agrega plantillas de issues en español"
git push origin main
```
