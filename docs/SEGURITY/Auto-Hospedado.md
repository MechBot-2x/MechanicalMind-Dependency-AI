# **implementación de Ejecutor Auto-Hospedado para MechanicalMind Dependency AI v2.0**

## **📌 Instrucciones Técnicas para el Equipo DevOps**

### **1. Configuración del Ejecutor Auto-Hospedado (Linux)**
**Objetivo:** Implementar un runner dedicado para mejorar la velocidad y seguridad de nuestros pipelines.

**Archivos clave:**
- `scripts/setup_runner.sh` (Nuevo script de automatización)
- `.github/workflows/runner-cleanup.yml` (Mantenimiento automático)

```bash
#!/bin/bash
# scripts/setup_runner.sh

RUNNER_NAME="mechmind-ai-runner-$(hostname)"
TOKEN="BPUT7UC27GU7YUQSSCAHBATH63QYI"  # Reemplazar con token real

echo "🔧 Configurando GitHub Actions Runner para MechanicalMind AI..."

# 1. Crear directorio
mkdir -p ~/actions-runner && cd ~/actions-runner

# 2. Descargar runner (versión específica para evitar breaking changes)
curl -o actions-runner-linux-x64-2.323.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.323.0/actions-runner-linux-x64-2.323.0.tar.gz

# 3. Verificar integridad
echo "0dbc9bf5a58620fc52cb6cc0448abcca964a8d74b5f39773b7afcad9ab691e19  actions-runner-linux-x64-2.323.0.tar.gz" | shasum -a 256 -c

# 4. Extraer
tar xzf ./actions-runner-linux-x64-2.323.0.tar.gz

# 5. Configurar (modo desatendido)
./config.sh --unattended \
  --url https://github.com/mechmind-dwv/-MechanicalMind-Dependency-AI-v2.0- \
  --token $TOKEN \
  --name $RUNNER_NAME \
  --labels "ai,dependency-manager,linux" \
  --work "_work"

# 6. Instalar como servicio
sudo ./svc.sh install
sudo ./svc.sh start

echo "✅ Runner configurado correctamente como servicio"
```

### **2. Configuración del Workflow para Ejecutores Auto-Hospedados**
**Archivo:** `.github/workflows/dependency_ai.yml`

```yaml
name: MechanicalMind Dependency AI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  dependency-scan:
    runs-on: self-hosted
    strategy:
      matrix:
        python-version: ["3.10", "3.11"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Run Dependency Analyzer
      run: |
        python -m ai_core.dependency_analyzer --repo $GITHUB_REPOSITORY
        python -m ai_core.error_diagnosis_engine --log-path ./logs/
    
    - name: Upload Results
      uses: actions/upload-artifact@v3
      with:
        name: dependency-report
        path: |
          ./dependency_graph.json
          ./error_analysis.md
```

### **3. Políticas de Seguridad para Runners Auto-Hospedados**
**Documento:** `docs/SECURITY_POLICY.md` (Actualizado)

```markdown
## 🔒 Políticas para Ejecutores Auto-Hospedados

1. **Aislamiento de Red:**
   - Los runners deben estar en una VPC separada
   - Acceso SSH restringido solo a direcciones IP corporativas

2. **Rotación de Tokens:**
   - Los tokens de runners caducan cada 72 horas
   - Usar `scripts/rotate-token.sh` para renovación automática

3. **Monitorización:**
   - Alertas en CloudWatch para actividad anómala
   - Logs de ejecución cifrados en S3
```
## 📊 Dashboard de Monitoreo (Opcional)

**Recomendación: Implementar Grafana con:**

**Métricas Clave:**

* Tiempo de ejecución promedio
* Uso de CPU/Memoria
* Tasa de fallos

**Alertas:**

Se recomienda configurar alertas en Grafana basadas en las métricas clave. Para la configuración inicial de alertas en AWS CloudWatch, puedes utilizar el siguiente script:

```bash
# scripts/monitoring_alerts.sh
aws cloudwatch put-metric-alarm \
  --alarm-name "HighRunnerCPU" \
  --metric-name "CPUUtilization" \
  --namespace "GitHubRunners" \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
  
### **4. Automatización de Mantenimiento**
**Archivo:** `.github/workflows/runner-cleanup.yml`

```yaml
name: Runner Maintenance

on:
  schedule:
    - cron: '0 3 * * *'  # Diario a las 3 AM

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
    - name: Cleanup old runners
      uses: actions/runner-cleanup@v1
      with:
        token: ${{ secrets.GH_RUNNER_CLEANUP_TOKEN }}
        max-age: 24h  # Eliminar runners inactivos >24h
```

## **📊 Dashboard de Monitoreo (Opcional)**
**Recomendación:** Implementar Grafana con:

1. **Métricas Clave:**
   - Tiempo de ejecución promedio
   - Uso de CPU/Memoria
   - Tasa de fallos

2. **Alertas:**
   ```bash
   # scripts/monitoring_alerts.sh
   aws cloudwatch put-metric-alarm \
     --alarm-name "HighRunnerCPU" \
     --metric-name "CPUUtilization" \
     --namespace "GitHubRunners" \
     --threshold 80 \
     --comparison-operator GreaterThanThreshold
   ```

## **💼 Checklist de Implementación**

| Tarea | Responsable | Estado |
|-------|------------|--------|
| Instalar runner en servidor dedicado | DevOps | ⏳ |
| Configurar VPC aislada | Networking | ✅ |
| Implementar rotación automática de tokens | Security | ⏳ |
| Migrar workflows a self-hosted | CI/CD Team | 🚀 |

**⚠️ Nota:** Todos los runners deben estar registrados en `INFRA-123` (Jira) para tracking.

---

**✅ Firmado:**  
**El Arquitecto DevOps** 🔧  
*"Construyendo la infraestructura del futuro, hoy."*
