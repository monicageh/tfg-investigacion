import json

# Cargar el archivo JSON original
input_file = 'pasapalabra_questions_to_model.json'
output_file = 'pasapalabra_questions_modified.json'

# Cargar el archivo
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Modificar el campo 'pregunta' en cada entrada
for entry in data:
    # Obtener la primera palabra correcta de 'respuesta_correcta'
    correct_word = entry.get('respuesta_correcta', '')
    if correct_word:
        first_letter = correct_word[0][0].upper()  # Primera letra de la primera palabra
        # Modificar el campo 'pregunta' agregando "Empieza por la {primera letra}"
        entry['pregunta'] = f"Empieza por la {first_letter}: {entry['pregunta']}"

# Guardar el JSON modificado
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"El archivo modificado se ha guardado en: {output_file}")
