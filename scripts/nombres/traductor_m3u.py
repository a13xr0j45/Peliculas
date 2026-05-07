import re
import requests
import time

# --- CONFIGURACIÓN ---
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2ZjZhYzk1OGU5ZTk0YzRjNDIzNzFlYmJhNThmNGUwMCIsIm5iZiI6MTMyMDYzOTY4OS4wLCJzdWIiOiI0ZWI3NWNjOTVlNzNkNjU1YWEwMDE3NDYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.UNIP3Eq8LfLCqZJXx64FE9PLot-O_aIF6sRUOhtbOT4"
ARCHIVO_ENTRADA = "1.m3u"
ARCHIVO_SALIDA = "2.m3u"
IDIOMA_DESTINO = "es-MX"

def limpiar_nombre(nombre):
    # Elimina contenido entre [] y entre ()
    nombre_limpio = re.sub(r'\[.*?\]|\(.*?\)', '', nombre)
    # Limpia espacios extra resultantes
    return " ".join(nombre_limpio.split()).strip()

def obtener_titulo_espanol(nombre_sucio):
    nombre_busqueda = limpiar_nombre(nombre_sucio)
    
    # Si al limpiar queda vacío (caso raro), usamos el original
    if not nombre_busqueda:
        return nombre_sucio

    url = "https://themoviedb.org"
    params = {
        "api_key": API_KEY,
        "query": nombre_busqueda,
        "language": IDIOMA_DESTINO
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get("results"):
            # Priorizamos el primer resultado de la búsqueda
            res = data["results"][0]
            # TMDb usa 'title' para películas y 'name' para series
            nuevo_nombre = res.get("title") or res.get("name")
            return nuevo_nombre
    except Exception:
        pass
    
    return nombre_sucio # Si hay error o no hay resultados, no cambia nada

def procesar_m3u():
    try:
        with open(ARCHIVO_ENTRADA, "r", encoding="utf-8") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ARCHIVO_ENTRADA}")
        return

    nuevas_lineas = []
    print(f"Iniciando traducción...")

    for linea in lineas:
        if linea.startswith("#EXTINF"):
            # Separamos la metadata del nombre por la última coma
            partes = linea.rsplit(',', 1)
            if len(partes) == 2:
                metadatos = partes[0]
                nombre_actual = partes[1].strip()
                
                print(f"Procesando: {nombre_actual}")
                nombre_es = obtener_titulo_espanol(nombre_actual)
                
                nuevas_lineas.append(f"{metadatos},{nombre_es}\n")
                time.sleep(0.25) # Respetar límites de la API
                continue
        
        nuevas_lineas.append(linea)

    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.writelines(nuevas_lineas)
    
    print(f"\n¡Hecho! Lista guardada en {ARCHIVO_SALIDA}")

if __name__ == "__main__":
    if API_KEY == "TU_API_KEY_AQUI":
        print("Recuerda configurar tu API KEY de TMDb en el script.")
    else:
        procesar_m3u()
