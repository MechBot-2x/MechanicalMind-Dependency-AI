## 🧩 Architecture Overview

```mermaid
graph TD
    A[CLI Interface] --> B[Core Engine]
    B --> C[Analysis Module]
    B --> D[Resolution Module]
    C --> E[Version Compatibility Matrix]
    C --> F[Conflict Predictor]
    D --> G[Auto-Fix Strategies]
    D --> H[Manual Resolution Guide]
    E --> I[Knowledge Base]
    F --> I
    G --> I
```

## ⚙️ Installation

### Quick Start (Linux/macOS)
```bash
curl -sSL https://install.mechmind.ai | bash
```

### Python Package
```bash
pip install mechmind-ai
```

### Docker Image
```bash
docker pull mechmind/ai-dependency:v3
```
