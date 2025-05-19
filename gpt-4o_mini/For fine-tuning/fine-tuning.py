import openai
from openai import OpenAI
import json

openai.api_key = 'my_api_key'

with open('pasapalabra.txt') as f:
    text = [line for line in f]
text[:10]

def formatear_ejemplo(lista_mensajes, system_message=None):
    messages = []

    # Incluir primero el mensaje de sistema
    if system_message:
        messages.append({
            "role": "system",
            "content": system_message
        })

    # Iterar por la lista de mensajes
    for mensaje in lista_mensajes:
        # Separar los mensajes por los dos puntos y el espacio
        partes = mensaje.split(': ', maxsplit=1)

        #Controlar si alguna línea no cumple el patrón
        if len(partes) < 2:
            continue

        # Identificar el rol y content
        role = partes[0].strip()
        content = partes[1].strip()

        # Formatear el mensaje
        message = {
            "role": role,
            "content": content
        }

        #Agregar el mensaje a la lista
        messages.append(message)

    # Crear diccionario final
    dict_final = {
        "messages": messages
    }

    # print(dict_final)

    return dict_final


system_message = 'Eres un concursante de un programa llamado Pasapalabra. \
El concurso consiste en que yo te digo una definicion y tu tienes que encontrar una unica palabra que cumpla con dos cosas: \
La definicion y antes de darte la definicion te indicare o la letra por la que comienza la palabra de la respuesta \
o una letra que contiene la palabra de la respuesta y la respuesta debe cumplir ambos criterios. \
En el caso de que no sepas cual es la respuesta, utiliza la palabra PASAPALABRA.'

dataset = []

ejemplo = []
for line in text:
  if line == '-\n':
    ejemplo_formateado = formatear_ejemplo(lista_mensajes=ejemplo,
                                            system_message=system_message)

    dataset.append(ejemplo_formateado)
    ejemplo = []
    continue

  ejemplo.append(line)

# Escribir el dataset en un archivo JSONL
def save_to_jsonl(dataset, file_path):
    with open(file_path, 'w') as file:
        for ejemplo in dataset:
            json_line = json.dumps(ejemplo, ensure_ascii=False)
            file.write(json_line + '\n')

#Guardar train full
save_to_jsonl(dataset, 'pasapalabra.jsonl')

# Escribir el dataset en un archivo JSON
with open('dataset_pasapalabra.json', 'w') as json_file:
    json.dump(dataset, json_file, indent=4)

# UPLOAD FILES
train_full_response_file = openai.files.create(
    file=open('pasapalabra.jsonl','rb'),
    purpose='fine-tune'
)


print(f'id: {train_full_response_file.id}')

# Creación del Fine-Tuning
response = openai.fine_tuning.jobs.create(
    training_file=train_full_response_file.id,
    model="gpt-4o-mini-2024-07-18",
    suffix='tfg-pasapalabra-4o',
    hyperparameters={'n_epochs':4}
)


print(response)
