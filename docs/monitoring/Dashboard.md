Dashboard de Monitoreo (Opcional)
Recomendación: Implementar Grafana con:

Métricas Clave:

Tiempo de ejecución promedio
Uso de CPU/Memoria
Tasa de fallos
Alertas:

# scripts/monitoring_alerts.sh
aws cloudwatch put-metric-alarm \
  --alarm-name "HighRunnerCPU" \
  --metric-name "CPUUtilization" \
  --namespace "GitHubRunners" \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
