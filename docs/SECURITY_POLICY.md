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
