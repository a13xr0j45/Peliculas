#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys

def capitalize_title(title):
    """
    Capitaliza cada palabra de un título.
    - Convierte la primera letra de cada palabra a mayúscula.
    - El resto de letras a minúscula.
    - Maneja correctamente palabras con apóstrofes y guiones.
    """
    # Lista de palabras que normalmente no se capitalizan (en minúscula)
    # Puedes personalizar esta lista según tus necesidades
    lowercase_words = {'de', 'la', 'el', 'los', 'las', 'y', 'o', 'u', 'con', 'sin', 
                       'por', 'para', 'un', 'una', 'unos', 'unas', 'al', 'del'}
    
    # Separar la cadena en palabras y no-palabras (espacios, puntuación)
    parts = re.split(r'(\W+)', title)
    
    result_parts = []
    for i, part in enumerate(parts):
        # Si es una palabra (alfabética)
        if re.match(r'^\w+$', part, re.UNICODE):
            word_lower = part.lower()
            # Si es la primera palabra o no está en la lista de minúsculas
            if i == 0 or word_lower not in lowercase_words:
                result_parts.append(part[0].upper() + part[1:].lower())
            else:
                result_parts.append(word_lower)
        else:
            result_parts.append(part)
    
    return ''.join(result_parts)

def extract_title_from_path(filepath):
    """
    Extrae el título del nombre del archivo sin extensión.
    """
    filename = os.path.basename(filepath)
    title = os.path.splitext(filename)[0]
    # Reemplazar guiones bajos o puntos por espacios
    title = title.replace('_', ' ').replace('.', ' ')
    # Eliminar múltiples espacios
    title = re.sub(r'\s+', ' ', title).strip()
    return title

def process_m3u_file(input_file, output_file=None):
    """
    Procesa un archivo .m3u y capitaliza los títulos.
    Mantiene las rutas de archivo intactas pero capitaliza el título mostrado.
    
    Para archivos .m3u estándar (solo rutas):
        #EXTINF: segundos, título_original
        ruta/del/archivo.mp3
    
    Para archivos .m3u extendido:
        #EXTINF: segundos, título_original
        ruta/del/archivo.mp3
    """
    if output_file is None:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_capitalized{ext}"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # Fallback a latin-1 si UTF-8 falla
        with open(input_file, 'r', encoding='latin-1') as f:
            lines = f.readlines()
    
    output_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i].rstrip('\n')
        
        # Detectar línea EXTINF (título)
        if line.startswith('#EXTINF:'):
            # Extraer el título después de la coma
            parts = line.split(',', 1)
            if len(parts) == 2:
                extinf_part = parts[0]
                original_title = parts[1]
                capitalized_title = capitalize_title(original_title)
                output_lines.append(f"{extinf_part},{capitalized_title}\n")
            else:
                output_lines.append(line + '\n')
            
            # La siguiente línea es la ruta del archivo (se copia sin cambios)
            if i + 1 < len(lines):
                output_lines.append(lines[i + 1])
                i += 2
                continue
            else:
                i += 1
                continue
        else:
            # Línea normal (comentario o ruta)
            output_lines.append(line + '\n')
            i += 1
    
    # Escribir archivo de salida
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print(f"✓ Archivo procesado: {input_file}")
    print(f"✓ Archivo guardado como: {output_file}")
    return output_file

def main():
    if len(sys.argv) < 2:
        print("Uso: python capitalizar_m3u_titulos.py <archivo.m3u> [archivo_salida.m3u]")
        print("\nEjemplo:")
        print("  python capitalizar_m3u_titulos.py playlist.m3u")
        print("  python capitalizar_m3u_titulos.py playlist.m3u playlist_capitalized.m3u")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Error: El archivo {input_file} no existe.")
        sys.exit(1)
    
    process_m3u_file(input_file, output_file)

if __name__ == "__main__":
    main()