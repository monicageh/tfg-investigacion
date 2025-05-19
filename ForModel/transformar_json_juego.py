import json

# Ruta al archivo original
input_file = 'pasapalabra_questions_modified.json'
# Ruta al archivo que se generará
output_file = 'roscos.json'

# Cargar el archivo JSON original
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Crear una lista para almacenar los roscos
roscos = []

# Agrupar las preguntas en bloques de 25 palabras por rosco
rosco_size = 25
for i in range(0, len(data), rosco_size):
    rosco_data = data[i:i+rosco_size]
    
    words = []
    for question in rosco_data:
        pregunta = question['pregunta']
        
        # Comprobar si es "Empieza por la" o "Contiene la"
        if "Empieza por la" in pregunta:
            letter = pregunta[15]  # Extraer la letra después de "Empieza por la "
        elif "Contiene la" in pregunta:
            letter = pregunta[14]  # Extraer la letra después de "Contiene la "
        else:
            letter = "?"  # Caso inesperado, usar un valor predeterminado

        correct_words = question['respuesta_correcta']
        definition = pregunta
        
        words.append({
            "letter": letter,
            "correctWords": correct_words,
            "definition": definition
        })

    rosco = {
        "_id": {"$oid": "unique_rosco_id"},  # Puedes usar un generador de IDs único
        "words": words,
        "_class": "upm.etsit.pasapalabra.model.Rosco"
    }
    
    roscos.append(rosco)

# Guardar los roscos en un nuevo archivo JSON
with open(output_file, 'w', encoding='utf-8') as out_file:
    json.dump(roscos, out_file, ensure_ascii=False, indent=4)

print(f"Archivo guardado en: {output_file}")
