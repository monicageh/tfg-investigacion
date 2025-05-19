import json
import os

# Define la ruta al archivo JSON
file_path = os.path.join('english', 'defsEnglishToFineTuning.json')

# Carga el JSON
with open(file_path) as f:
    data = json.load(f)

# Abre un archivo para escribir el resultado
with open('defsEnglish.txt', 'w') as f:
    # Itera sobre cada objeto en el JSON
    for item in data:
        pregunta = item['pregunta']
        respuesta_correcta = item['respuesta_correcta']

        # Escribe la pregunta y la respuesta en el formato deseado
        f.write(f"user: {pregunta}.\n")
        f.write(f"assistant: {respuesta_correcta}\n-\n")
