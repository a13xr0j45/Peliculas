import re

def limpiar_texto(texto):
    # Elimina contenido dentro de () y [] incluyendo los símbolos
    limpio = re.sub(r'\(.*?\)|\[.*?\]', '', texto)
    # Quita espacios extra y pasa a minúsculas
    return limpio.strip().lower()

def comparar_solo_en_1():
    encoding_config = 'latin-1' 
    
    try:
        with open('1.txt', 'r', encoding=encoding_config) as f1, \
             open('2.txt', 'r', encoding=encoding_config) as f2:
            
            # Cargamos ambos archivos aplicando la limpieza
            lineas1 = set(limpiar_texto(linea) for linea in f1 if linea.strip())
            lineas2 = set(limpiar_texto(linea) for linea in f2 if linea.strip())

        # RESTA: Elementos que están en lineas1 pero NO en lineas2
        solo_en_1 = lineas1 - lineas2

        # Guardar el resultado en 3.txt
        with open('3.txt', 'w', encoding=encoding_config) as f3:
            for item in sorted(solo_en_1):
                if item:
                    f3.write(f"{item}\n")

        print("-" * 30)
        print(f"PROCESO COMPLETADO")
        print(f"Archivos encontrados solo en Lista 1: {len(solo_en_1)}")
        print(f"Detalle guardado en 3.txt")
        print("-" * 30)

    except FileNotFoundError:
        print("Error: Asegúrate de que 1.txt y 2.txt existan.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    comparar_solo_en_1()
