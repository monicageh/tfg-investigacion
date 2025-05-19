import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import openai

openai_api_key = 'my_api_key'
openai.api_key = openai_api_key

# Cargar las preguntas desde el archivo JSON
#file_path = "defsRAE_for_finetuning_model.json"
file_path = "pasapalabra_questions_to_model.json"
with open(file_path, "r", encoding="utf-8") as file:
    questions = json.load(file)


model_name = "ft:gpt-4o-mini-2024-07-18:personal::BHaoIhOf"
chat = ChatOpenAI(model=model_name, openai_api_key=openai_api_key, temperature=0.0)

# Iterar sobre cada pregunta en la lista
for current_question in questions:
    system_message = 'Eres un concursante de un programa llamado Pasapalabra. \
    El concurso consiste en que yo te digo una definicion y tu tienes que encontrar una unica palabra que cumpla con dos cosas: \
    La primera, la definicion y la segunda, antes de darte la definicion te indicare o la letra por la que comienza la palabra de la respuesta \
    o una letra que contiene la palabra de la respuesta y la respuesta debe cumplir OBLIGATORIAMENTE ambos criterios. \
    En el caso de que no sepas cual es la respuesta, utiliza la palabra PASAPALABRA.'

    print(current_question["pregunta"])
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=current_question["pregunta"])
    ]

    response = chat(messages)
    print(response.content)

    # Guardar la respuesta en el campo "respuesta_chatgpt"
    current_question["respuesta_chatgpt"] = response.content

# Guardar los cambios en el archivo JSON
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(questions, file, indent=4)









