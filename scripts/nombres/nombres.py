import re

def clasificar_m3u(archivo_origen, archivo_final, archivo_excluidos):
    try:
        with open(archivo_origen, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo_origen}")
        return

    cabecera = lineas[0] if lineas and lineas[0].startswith("#EXTM3U") else "#EXTM3U\n"
    
    final_list = [cabecera]
    excluidos_list = [cabecera]

    # Iteramos saltando la cabecera
    i = 0
    if lineas and lineas[0].startswith("#EXTM3U"):
        i = 1

    while i < len(lineas):
        linea_actual = lineas[i]
        
        # Verificamos si es una línea de información de canal (#EXTINF)
        if linea_actual.startswith("#EXTINF"):
            # El bloque completo suele ser la info + la URL (siguiente línea)
            bloque = [linea_actual]
            if i + 1 < len(lineas):
                bloque.append(lineas[i+1])
            
            # Buscamos si contiene paréntesis () o corchetes []
            if re.search(r'[\(\)\[\]]', linea_actual):
                final_list.extend(bloque)
            else:
                excluidos_list.extend(bloque)
            
            i += 2 # Saltamos el bloque procesado
        else:
            i += 1 # Ignorar líneas vacías o extrañas

    # Guardar resultados
    with open(archivo_final, 'w', encoding='utf-8') as f:
        f.writelines(final_list)
    
    with open(archivo_excluidos, 'w', encoding='utf-8') as f:
        f.writelines(excluidos_list)

    print(f"Proceso terminado.\n- {archivo_final} generado.\n- {archivo_excluidos} generado.")

# Ejecutar la función
clasificar_m3u('origen.m3u', 'final.m3u', 'excluidos.m3u')
