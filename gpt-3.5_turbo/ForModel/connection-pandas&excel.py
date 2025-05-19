import pandas as pd

# Cargar datos desde un archivo JSON
with open('pasapalabra_questions.json', 'r') as file:
    data = pd.read_json(file)

# Especificar el nombre del archivo Excel que deseas crear
pasapalabra_questions = 'pasapalabra_questionsEJ.xlsx'

# Escribir el DataFrame en el archivo Excel
data.to_excel(pasapalabra_questions, index=False)

print(f'Se ha creado el archivo {pasapalabra_questions} correctamente.')
