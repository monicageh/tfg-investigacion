import json

# Ruta del archivo JSON
file_path = "ForModel/pasapalabra_questions_to_model.json"

# Cargar datos desde el archivo JSON
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Función para convertir a mayúsculas
def convertir_a_mayusculas(objeto):
    # Convertir respuesta_concursante
    if "respuesta_concursante" in objeto:
        objeto["respuesta_concursante"] = objeto["respuesta_concursante"].upper()

    # Convertir respuesta_chatgpt
    if "respuesta_chatgpt" in objeto:
        objeto["respuesta_chatgpt"] = objeto["respuesta_chatgpt"].upper()

    # Convertir respuesta_correcta
    if "respuesta_correcta" in objeto:
        objeto["respuesta_correcta"] = [respuesta.upper() for respuesta in objeto["respuesta_correcta"]]

    return objeto

# Aplicar la función a cada objeto en data
data = [convertir_a_mayusculas(obj) for obj in data]

# Guardar los cambios en el archivo JSON
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("Se han convertido las respuestas concursantes, respuestas de ChatGPT y respuestas correctas a mayúsculas correctamente.")
