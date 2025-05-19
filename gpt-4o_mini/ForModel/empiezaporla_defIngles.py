# Script de Python para procesar el archivo y agregar la primera letra de la palabra antes de la definición

def procesar_definiciones(archivo_entrada, archivo_salida):
    with open(archivo_entrada, 'r', encoding='utf-8') as f_in:
        lineas = f_in.readlines()
    
    with open(archivo_salida, 'w', encoding='utf-8') as f_out:
        # Iteramos por las líneas del archivo
        for i in range(0, len(lineas), 2):  # Tomamos de dos en dos (definición y palabra)
            if i+1 < len(lineas):  # Verificar que haya una palabra correspondiente
                definicion = lineas[i].strip()  # Remover saltos de línea y espacios
                palabra = lineas[i+1].strip()
                
                # Obtenemos la primera letra de la palabra
                primera_letra = palabra[0].upper()
                
                # Añadimos el texto modificado, seguido de la palabra en una nueva línea
                f_out.write(f"Starts with {primera_letra}: {definicion}\n")
                f_out.write(f"{palabra}\n")

# Llamamos a la función con los archivos de entrada y salida
archivo_entrada = 'defIngles.txt'  # Archivo de entrada con las definiciones y palabras
archivo_salida = 'defIngles_modificadas.txt'  # Archivo donde se guardará el resultado

procesar_definiciones(archivo_entrada, archivo_salida)

print(f"Archivo procesado y guardado en {archivo_salida}")
