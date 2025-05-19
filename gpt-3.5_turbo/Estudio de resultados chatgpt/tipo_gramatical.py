import json

# Cargar el archivo JSON
file_path = 'defsIngles_for_finetuning_model.json'  # Cambia a la ruta correcta si es necesario
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Clasificación de los tipos gramaticales basado en el rango de respuestas
for idx, item in enumerate(data):
    if idx < 25:
        item['tipo_gramatical'] = 'adjetivo'
    elif idx >= 175:
        item['tipo_gramatical'] = 'verbo'
    else:
        item['tipo_gramatical'] = 'sustantivo'

# Guardar los datos con el nuevo campo 'tipo_gramatical'
output_path = 'defsIngles_for_finetuning_model_updated.json'
with open(output_path, 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, ensure_ascii=False, indent=4)

print(f"Archivo actualizado guardado en {output_path}")
