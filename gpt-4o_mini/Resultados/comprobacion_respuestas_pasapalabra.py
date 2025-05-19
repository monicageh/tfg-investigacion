import json

# Ruta del archivo JSON
file_path = "../ForModel/pasapalabra_questions_to_model.json"  

# Función para comparar respuestas y guardar objetos completos
def comparar_respuestas(data, tipo_respuesta):
    respuestas_correctas = []

    for pregunta in data:
        id_pregunta = pregunta["id"]  # Obtener el ID original
        respuesta_correcta = pregunta["respuesta_correcta"]
        respuesta = pregunta[tipo_respuesta]

        if respuesta in respuesta_correcta:
            pregunta["id"] = id_pregunta  # Asignar el ID original al objeto
            respuestas_correctas.append(pregunta)  # Añadir objeto completo

    return respuestas_correctas

# Cargar datos desde el archivo JSON
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Calcular número total de preguntas
total_preguntas = len(data)

# Comparar respuestas_chatgpt
respuestas_correctas_chatgpt = comparar_respuestas(data, "respuesta_chatgpt")

# Guardar respuestas correctas de chatgpt en un archivo JSON
with open("respuestasCorrectasChatGPT_pasapalabra.json", "w", encoding="utf-8") as file:
    json.dump(respuestas_correctas_chatgpt, file, indent=4, ensure_ascii=False)

# Imprimir número de respuestas correctas de chatgpt
num_respuestas_correctas_chatgpt = len(respuestas_correctas_chatgpt)
print(f"\nNúmero de respuestas correctas de ChatGPT: {num_respuestas_correctas_chatgpt} de {total_preguntas} preguntas totales.")

# Comparar respuestas_concursante
respuestas_correctas_concursante = comparar_respuestas(data, "respuesta_concursante")

# Guardar respuestas correctas de concursante en un archivo JSON
with open("respuestasCorrectasConcursante.json", "w", encoding="utf-8") as file:
    json.dump(respuestas_correctas_concursante, file, indent=4, ensure_ascii=False)

# Imprimir número de respuestas correctas de concursante
num_respuestas_correctas_concursante = len(respuestas_correctas_concursante)
print(f"\nNúmero de respuestas correctas de Concursante: {num_respuestas_correctas_concursante} de {total_preguntas} preguntas totales.")
