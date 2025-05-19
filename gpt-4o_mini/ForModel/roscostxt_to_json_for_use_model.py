import json

# Leer el texto desde el archivo roscos.txt
with open('roscos.txt', 'r', encoding='utf-8') as file:
    texto = file.read()

# Dividir el texto en líneas
lineas = texto.strip().split('\n')

# Inicializar una lista para almacenar las preguntas en formato JSON
preguntas = []
id_pregunta = 1
pregunta_actual = {}

# Procesar cada línea del texto
for linea in lineas:
    # Buscar líneas que indiquen una nueva pregunta
    if linea.startswith("EMPIEZA POR ") or linea.startswith("CONTIENE LA "):
        if pregunta_actual:
            preguntas.append(pregunta_actual)
            pregunta_actual = {}

        # Extraer la categoría y la pregunta
        if ': ' in linea:
            categoria, pregunta = linea.split(': ', 1)
            pregunta_actual["id"] = str(id_pregunta)
            pregunta_actual["pregunta"] = pregunta.strip()
            id_pregunta += 1
        else:
            continue  # Saltar líneas que no tienen el formato esperado

    # Las siguientes líneas contienen las respuestas
    elif linea.strip() and pregunta_actual:
        # Verificar si es la respuesta correcta o la respuesta del concursante
        if linea.isupper():
            if "respuesta_correcta" not in pregunta_actual:
                pregunta_actual["respuesta_correcta"] = []
            pregunta_actual["respuesta_correcta"].append(linea.strip())
        else:
            pregunta_actual["respuesta_concursante"] = linea.strip()

# Agregar el campo respuesta_chatgpt vacío a cada pregunta
for pregunta in preguntas:
    pregunta["respuesta_chatgpt"] = ""

# Convertir la lista de preguntas a formato JSON
json_data = json.dumps(preguntas, indent=2, ensure_ascii=False)

# Escribir el JSON resultante en un archivo llamado pasapalabra_questions_for_finetuningModel.json
with open('pasapalabra_questions_for_finetuningModel.json', 'w', encoding='utf-8') as file:
    file.write(json_data)

print("Archivo pasapalabra_questions_for_finetuningModel.json generado exitosamente.")
