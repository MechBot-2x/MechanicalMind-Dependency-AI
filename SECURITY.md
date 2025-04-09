## **🛡 Versiones Soportadas**  

| Versión | Soporte            | Hasta        |
|---------|--------------------|--------------|
| 2.3.x   | ✅ Soporte completo | 31/03/2026  |
| 2.2.x   | ⚠️ Solo críticas   | 31/12/2025  |
| ≤ 2.1   | ❌ Sin soporte     | N/A         |

**Notas:**  
- Recibirás parches automáticos si usas `main` (v2.3.x)  
- Las versiones antiguas requieren actualización  

---

## **🚨 Reportar Vulnerabilidades**  
### **1. Métodos Seguros**  
```bash
# Usando nuestro script (preferido)
./scripts/reportar_vulnerabilidad.sh --tipo "inyección SQL"

# O por correo con PGP
echo "Detalle del problema" | gpg --encrypt -r seguridad@mechmind-dwv.com
