import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import openai

openai_api_key = 'my_api_key'
openai.api_key = openai_api_key

# Cargar las preguntas desde el archivo JSON en la carpeta english/ForModel
file_path = "defsIngles_for_finetuning_model.json"
with open(file_path, "r") as file:
    questions = json.load(file)

model_name = "ft:gpt-3.5-turbo-0125:personal:tfg-englishdefs:9bYPFicX"
chat = ChatOpenAI(model=model_name, openai_api_key=openai_api_key, temperature=0.0)

# Iterar sobre cada pregunta en la lista
for current_question in questions:
    system_message = 'You are a contestant on a show called Pasapalabra. \
The contest consists of me giving you a definition, and you have to find a single word that meets two criteria: \
the definition and the letter I will give you before the definition. The letter can either be the starting letter of the answer word \
or a letter contained in the answer word, and the answer must fulfill both criteria. \
If you dont know the answer, use the word PASAPALABRA.'

    print(current_question["pregunta"])
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=current_question["pregunta"])
    ]

    response = chat(messages)
    print(response.content)

    # Guardar la respuesta en el campo "respuesta_chatgpt"
    current_question["respuesta_chatgpt"] = response.content

# Guardar los cambios en el archivo JSON en la carpeta english/ForModel
with open(file_path, "w") as file:
    json.dump(questions, file, indent=4)
