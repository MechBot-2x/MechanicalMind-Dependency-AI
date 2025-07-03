RUNNER_NAME="mechmind-ai-runner-$(hostname)"
TOKEN=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  # Reemplazar con token real

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
