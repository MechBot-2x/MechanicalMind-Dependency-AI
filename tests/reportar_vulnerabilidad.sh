# 🚨 Reportar Vulnerabilidades
# Usando nuestro script (preferido)
./scripts/reportar_vulnerabilidad.sh --tipo "inyección SQL"

# O por correo con PGP
echo "Detalle del problema" | gpg --encrypt -r ia.mechnind@gmail.com
