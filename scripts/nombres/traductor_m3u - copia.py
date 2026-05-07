import re
import requests
import time

# --- CONFIGURACIÓN ---
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2ZjZhYzk1OGU5ZTk0YzRjNDIzNzFlYmJhNThmNGUwMCIsIm5iZiI6MTMyMDYzOTY4OS4wLCJzdWIiOiI0ZWI3NWNjOTVlNzNkNjU1YWEwMDE3NDYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.UNIP3Eq8LfLCqZJXx64FE9PLot-O_aIF6sRUOhtbOT4"
ARCHIVO_ENTRADA = "1.m3u"
ARCHIVO_SALIDA = "2.m3u"
IDIOMA_DESTINO = "es-MX"

def limpiar_nombre(nombre):
    # Elimina cualquier contenido dentro de corchetes [] y espacios sobrantes
    return re.sub(r'\[.*?\]', '', nombre).strip()

def obtener_titulo_espanol(nombre_sucio):
    nombre_limpio = limpiar_nombre(nombre_sucio)
    
    if not nombre_limpio:
        return nombre_sucio

    url = "https://themoviedb.org"
    params = {
        "api_key": API_KEY,
        "query": nombre_limpio,
        "language": IDIOMA_DESTINO
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get("results"):
            primer_resultado = data["results"][0]
            return primer_resultado.get("title") or primer_resultado.get("name")
    except Exception:
        pass
    
    return nombre_sucio # Retorna el original si falla o no encuentra nada

def procesar_m3u():
    try:
        with open(ARCHIVO_ENTRADA, "r", encoding="utf-8") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print(f"Error: No se encontró {ARCHIVO_ENTRADA}")
        return

    print(f"Procesando lista...")
    nuevas_lineas = []

    for linea in lineas:
        if linea.startswith("#EXTINF"):
            # Dividir por la última coma para extraer el nombre
            partes = linea.rsplit(',', 1)
            if len(partes) == 2:
                prefijo = partes[0]
                nombre_en = partes[1].strip()
                
                print(f"Buscando: {nombre_en}")
                nombre_es = obtener_titulo_espanol(nombre_en)
                
                nuevas_lineas.append(f"{prefijo},{nombre_es}\n")
                time.sleep(0.2) # Evitar baneo de la API
                continue
        
        nuevas_lineas.append(linea)

    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.writelines(nuevas_lineas)
    
    print(f"\nProceso terminado. Archivo guardado como {ARCHIVO_SALIDA}")

if __name__ == "__main__":
    if API_KEY == "TU_API_KEY_AQUI":
        print("Error: Necesitas poner tu API KEY de TMDb en el script.")
    else:
        procesar_m3u()
