import json

# Ruta del archivo JSON
file_path = "../ForModel/defsRAE_for_finetuning_model.json"

# Función para comparar respuestas chatgpt con respuestas correctas
def comparar_respuestas(data):
    respuestas_correctas_chatgpt = []
    respuestas_totales = len(data)

    for pregunta in data:
        id_pregunta = pregunta["id"]
        respuesta_correcta = pregunta["respuesta_correcta"]
        respuesta_chatgpt = pregunta["respuesta_chatgpt"]

        if respuesta_chatgpt in respuesta_correcta:
            pregunta["id"] = id_pregunta  # Mantener el ID original en el objeto
            respuestas_correctas_chatgpt.append(pregunta)  # Añadir objeto completo

    return respuestas_correctas_chatgpt, respuestas_totales

# Cargar datos desde el archivo JSON
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Comparar respuestas chatgpt con respuestas correctas
respuestas_correctas_chatgpt, total_preguntas = comparar_respuestas(data)

# Imprimir número de respuestas correctas de chatgpt y total de preguntas
num_respuestas_correctas_chatgpt = len(respuestas_correctas_chatgpt)
print(f"Número de respuestas correctas de ChatGPT: {num_respuestas_correctas_chatgpt} de {total_preguntas} preguntas totales.")

# Guardar respuestas correctas de chatgpt en un archivo JSON
output_file = "respuestasCorrectasChatGPT_definicionesRAE.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(respuestas_correctas_chatgpt, file, indent=4, ensure_ascii=False)

print(f"Se han guardado las respuestas correctas de ChatGPT en '{output_file}'.")
