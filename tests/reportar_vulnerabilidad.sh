🚨 Reportar Vulnerabilidades
1. Métodos Seguros
# Usando nuestro script (preferido)
./scripts/reportar_vulnerabilidad.sh --tipo "inyección SQL"

# O por correo con PGP
echo "Detalle del problema" | gpg --encrypt -r seguridad@mechmind-dwv.com
