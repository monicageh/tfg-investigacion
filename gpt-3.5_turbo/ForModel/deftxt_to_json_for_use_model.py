import json

# Función para limpiar y dividir el texto en preguntas y respuestas
def procesar_texto(texto):
    lineas = texto.strip().split('\n')
    preguntas = []
    id_pregunta = 0

    for i, linea in enumerate(lineas):
        if i % 2 == 0:  # Líneas pares son preguntas
            pregunta_actual = {}
            pregunta_actual["id"] = str(id_pregunta)
            pregunta_actual["pregunta"] = linea.strip()
            id_pregunta += 1
        else:  # Líneas impares son respuestas
            pregunta_actual = {
                "id": str(id_pregunta),
                "pregunta": pregunta_actual["pregunta"],
                "respuesta_correcta": linea.strip(),
                "respuesta_chatgpt": ""
            }
            preguntas.append(pregunta_actual)

    return preguntas

# Leer el texto desde el archivo defRae.txt
with open('defRae.txt', 'r', encoding='utf-8') as file:
    texto = file.read()

# Procesar el texto en formato de preguntas y respuestas
preguntas = procesar_texto(texto)

# Convertir la lista de preguntas a formato JSON
json_data = json.dumps(preguntas, indent=2, ensure_ascii=False)

# Escribir el JSON resultante en un archivo llamado pasapalabra_questions_for_finetuningModel.json
with open('defsRAE_for_finetuning_model.json', 'w', encoding='utf-8') as file:
    file.write(json_data)

print("Archivo defsRAE_for_finetuning_model.json generado exitosamente.")
