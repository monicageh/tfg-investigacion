import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# Paso 1: Cargar los datos desde los archivos JSON
roscos_df = pd.read_json('pasapalabra_questions_to_model.json')
rae_df = pd.read_json('defsRAE_for_finetuning_model.json')
ingles_df = pd.read_json('defsIngles_for_finetuning_model.json')

# Paso 2: Calcular la tasa de aciertos en bruto
def calcular_tasa_aciertos(df):
    aciertos = df.apply(lambda x: x['respuesta_chatgpt'] in x['respuesta_correcta'], axis=1).sum()
    total = len(df)
    tasa_aciertos = aciertos / total
    return tasa_aciertos

tasa_aciertos_roscos = calcular_tasa_aciertos(roscos_df)
tasa_aciertos_rae = calcular_tasa_aciertos(rae_df)
tasa_aciertos_ingles = calcular_tasa_aciertos(ingles_df)

# Imprimir tasas de aciertos
print("Tasa de aciertos en Roscos:", tasa_aciertos_roscos)
print("Tasa de aciertos en RAE:", tasa_aciertos_rae)
print("Tasa de aciertos en Inglés:", tasa_aciertos_ingles)

# Generar gráficas para visualizar los resultados
tasas_aciertos = [tasa_aciertos_roscos, tasa_aciertos_rae, tasa_aciertos_ingles]
etiquetas = ['Roscos', 'RAE', 'Inglés']
colores = ['#ff6666', '#003f88', '#33cc66']

plt.bar(etiquetas, tasas_aciertos, color=colores)
plt.xlabel('Categoría')
plt.ylabel('Tasa de Aciertos (%)')
plt.title('CHATGPT-4o MINI')
plt.gca().yaxis.set_major_formatter(PercentFormatter(1.0))  # Formato porcentaje
plt.ylim(0, 1)  # Asegura que el eje y esté entre 0% y 100%
plt.tight_layout()
plt.show()
