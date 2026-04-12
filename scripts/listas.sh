#!/bin/bash

# Archivos de entrada y salida
INPUT="pelis.txt"
OUTPUT="pelis_sin_duplicados.txt"

# Verificar que el archivo de entrada existe
if [ ! -f "$INPUT" ]; then
    echo "❌ Error: No se encuentra el archivo $INPUT"
    exit 1
fi

# Archivos temporales
TEMP_INFO=$(mktemp)
TEMP_URLS=$(mktemp)

# Variables de control
declare -A urls_vistas
contador=0
duplicados=0

# Leer línea por línea
while IFS= read -r linea; do
    # Si la línea comienza con #EXTINF, guardamos la info y esperamos la URL
    if [[ "$linea" == \#EXTINF* ]]; then
        info_line="$linea"
        # Leer la siguiente línea (la URL)
        if IFS= read -r url_line; then
            # Verificar si la URL ya fue vista
            if [[ -z "${urls_vistas[$url_line]}" ]]; then
                # URL nueva - la guardamos
                urls_vistas["$url_line"]=1
                echo "$info_line" >> "$TEMP_INFO"
                echo "$url_line" >> "$TEMP_URLS"
                ((contador++))
            else
                # URL duplicada - la saltamos
                ((duplicados++))
            fi
        else
            # No hay URL después de #EXTINF (caso raro)
            echo "$info_line" >> "$TEMP_INFO"
        fi
    else
        # Línea que no es #EXTINF (como #EXTM3U o líneas sueltas)
        # Solo la agregamos si no estamos dentro de una entrada duplicada
        if [[ -z "$info_line" ]] || [[ -n "${urls_vistas[$linea]}" ]]; then
            # Es una línea suelta como #EXTM3U
            echo "$linea" >> "$TEMP_INFO"
        fi
    fi
done < "$INPUT"

# Combinar los archivos temporales manteniendo el orden
{
    # Primera línea (normalmente #EXTM3U)
    head -n 1 "$INPUT" 2>/dev/null | grep -q "^#EXTM3U" && head -n 1 "$INPUT"
    
    # Resto de las entradas
    paste -d '\n' "$TEMP_INFO" "$TEMP_URLS" 2>/dev/null
} | grep -v '^$' > "$OUTPUT"

# Limpiar archivos temporales
rm -f "$TEMP_INFO" "$TEMP_URLS"

# Resultado
echo "✅ Archivo limpiado guardado como: $OUTPUT"
echo "📊 URLs únicas conservadas: $contador"
echo "🗑️  Duplicados eliminados: $duplicados"