#!/usr/bin/env bash

# Ruta local del archivo version.txt
LOCAL_VERSION_FILE="./version.txt"

# URL del version.txt en GitHub (raw)
REMOTE_VERSION_URL="https://raw.githubusercontent.com/aresmartius/cordic/main/version.txt"

# Comprobación de existencia local
if [[ ! -f "$LOCAL_VERSION_FILE" ]]; then
    echo "No existe version.txt local. Crea uno o descarga el proyecto."
    exit 1
fi

# Leer versión local
LOCAL_VERSION=$(cat "$LOCAL_VERSION_FILE")

# Obtener versión remota
REMOTE_VERSION=$(curl -s "$REMOTE_VERSION_URL")

if [[ -z "$REMOTE_VERSION" ]]; then
    echo "No se pudo obtener la versión remota."
    exit 1
fi

# Comparar
if [[ "$LOCAL_VERSION" == "$REMOTE_VERSION" ]]; then
    echo "✔ Tienes la última versión ($LOCAL_VERSION)."
    exit 0
else
    echo "✘ Tu versión local es: $LOCAL_VERSION"
    echo "✔ La versión remota es: $REMOTE_VERSION"
    echo -n "¿Quieres descargar la nueva versión? (s/n): "
    read -r ANS

    if [[ "$ANS" == "s" || "$ANS" == "S" ]]; then
    	echo "Descargando nueva versión..."

    	# Definir URLs de los archivos en raw
    	REMOTE_BASE_URL="https://raw.githubusercontent.com/aresmartius/cordic/main"
    
    	curl -L -o "version.txt" "$REMOTE_BASE_URL/version.txt"
    	curl -L -o "cordic.ipynb" "$REMOTE_BASE_URL/cordic.ipynb"
    	curl -L -o "cordic.py" "$REMOTE_BASE_URL/cordic.py"
    	curl -L -o "cordic.exe" "$REMOTE_BASE_URL/cordic.exe"

    	echo "Actualizado."
    fi

fi
