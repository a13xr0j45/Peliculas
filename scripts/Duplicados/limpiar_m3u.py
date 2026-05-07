import re

def limpiar_m3u(archivo_entrada, archivo_salida):
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    nuevas_lineas = []
    urls_vistas = set()
    i = 0
    total = len(lineas)

    while i < total:
        linea = lineas[i].rstrip('\n')
        if linea.startswith('#EXTINF'):
            # Guardamos la línea de información
            info_line = linea
            i += 1
            if i < total:
                url_line = lineas[i].rstrip('\n')
                # Verificamos si la URL ya fue vista
                if url_line not in urls_vistas:
                    urls_vistas.add(url_line)
                    nuevas_lineas.append(info_line + '\n')
                    nuevas_lineas.append(url_line + '\n')
                # Si ya existe, simplemente saltamos esta entrada duplicada
                i += 1
        else:
            # Línea que no es parte de una entrada normal (p.ej., #EXTM3U)
            nuevas_lineas.append(linea + '\n')
            i += 1

    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.writelines(nuevas_lineas)

    print(f"✅ Archivo limpiado guardado como: {archivo_salida}")
    print(f"📊 URLs únicas conservadas: {len(urls_vistas)}")

# Uso
limpiar_m3u('pelis.txt', 'pelis_sin_duplicados.txt')