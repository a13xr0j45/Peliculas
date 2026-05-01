import re

def limpiar_texto(texto):
    # Elimina contenido dentro de () y [] incluyendo los paréntesis/corchetes
    # El patrón r'\(.*?\)|\[.*?\]' busca estos pares y los borra
    limpio = re.sub(r'\(.*?\)|\[.*?\]', '', texto)
    # Quitamos espacios extra que puedan quedar y pasamos a minúsculas
    return limpio.strip().lower()

def comparar_listas_final():
    encoding_config = 'latin-1' 
    
    try:
        with open('1.txt', 'r', encoding=encoding_config) as f1, \
             open('2.txt', 'r', encoding=encoding_config) as f2:
            
            # Limpiamos cada línea antes de meterla al set de comparación
            lineas1 = set(limpiar_texto(linea) for linea in f1 if linea.strip())
            lineas2 = set(limpiar_texto(linea) for linea in f2 if linea.strip())

        # Diferencia: lo que no está en ambos
        diferencia = lineas1.symmetric_difference(lineas2)

        with open('3.txt', 'w', encoding=encoding_config) as f3:
            # Filtramos para no escribir líneas vacías si el nombre era solo (algo)
            for item in sorted(diferencia):
                if item:
                    f3.write(f"{item}\n")

        print(f"Comparación terminada.")
        print(f"Se ignoraron paréntesis/corchetes y mayúsculas.")
        print(f"Diferencias guardadas en 3.txt: {len(diferencia)}")

    except FileNotFoundError:
        print("Error: Asegúrate de tener 1.txt y 2.txt en la carpeta.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    comparar_listas_final()
