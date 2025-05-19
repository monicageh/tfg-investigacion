import pandas as pd
import json
import matplotlib.pyplot as plt

# Rutas a los archivos
ruta_json = 'defsRAE_for_finetuning_model_updated.json'
ruta_excel = 'familiarity.xlsx'

# Paso 1: Cargar el archivo JSON
with open(ruta_json, 'r', encoding='utf-8') as file:
    data_json = json.load(file)

# Extraer palabra correcta y respuestas de ChatGPT y concursante
palabras_data = []
for item in data_json:
    correcta = item.get('respuesta_correcta')
    chatgpt = item.get('respuesta_chatgpt')
    concursante = item.get('respuesta_concursante')
    if correcta:
        palabra = correcta.lower().strip()
        acierto_chatgpt = int(chatgpt and chatgpt.lower().strip() == palabra)
        acierto_concursante = int(concursante and concursante.lower().strip() == palabra)
        palabras_data.append({
            'palabra': palabra,
            'acierto_chatgpt': acierto_chatgpt,
            'acierto_concursante': acierto_concursante
        })

df_aciertos = pd.DataFrame(palabras_data)

# Paso 2: Cargar el archivo Excel de familiaridad
familiaridad = pd.read_excel(ruta_excel, sheet_name=0)
familiaridad.columns = [col.lower() for col in familiaridad.columns]
familiaridad['word'] = familiaridad['word'].str.lower().str.strip()

# Paso 3: Unir con las familiaridades
df = pd.merge(df_aciertos, familiaridad[['word', 'gpt_dom']], left_on='palabra', right_on='word', how='left')
df = df.drop(columns=['word'])
df.rename(columns={'gpt_dom': 'familiaridad_es'}, inplace=True)

# Paso 4: Clasificar en niveles
min_valor = df['familiaridad_es'].min(skipna=True)
max_valor = df['familiaridad_es'].max(skipna=True)

if min_valor is not None and max_valor is not None and min_valor >= 0 and max_valor <= 6.5:
    bins = [0, 1, 2, 3, 4, 5, 6, 6.5]
    labels = ['1', '2', '3', '4', '5', '6', '7']
else:
    bins = [1, 2, 3, 4, 5, 6, 7, 8]
    labels = ['1', '2', '3', '4', '5', '6', '7']

df['nivel'] = pd.cut(df['familiaridad_es'], bins=bins, labels=labels, include_lowest=True)
df['nivel'] = df['nivel'].cat.add_categories(['0']).fillna('0')

# Paso 5: Calcular porcentajes de aciertos por nivel
aciertos_chatgpt = df.groupby('nivel')['acierto_chatgpt'].sum()
aciertos_concursante = df.groupby('nivel')['acierto_concursante'].sum()
total_por_nivel = df.groupby('nivel').size()

porcentaje_chatgpt = (aciertos_chatgpt / total_por_nivel) * 100
porcentaje_concursante = (aciertos_concursante / total_por_nivel) * 100

# Paso 6: Imprimir resumen
print("\nDistribución por niveles de familiaridad:")
for nivel in total_por_nivel.index:
    if nivel != "0":
        rango_inicio = bins[labels.index(nivel)]
        rango_fin = bins[labels.index(nivel) + 1]
        print(f"Nivel {nivel}: {total_por_nivel[nivel]} palabras - Rango: {rango_inicio} a {rango_fin} - "
              f"Aciertos ChatGPT: {porcentaje_chatgpt[nivel]:.2f}%, Concursante: {porcentaje_concursante[nivel]:.2f}%")
    else:
        print(f"Nivel 0: {total_por_nivel[nivel]} palabras - "
              f"Aciertos ChatGPT: {porcentaje_chatgpt[nivel]:.2f}%, Concursante: {porcentaje_concursante[nivel]:.2f}%")

# Paso 7: Gráfico de barras comparativo

import numpy as np

niveles = list(total_por_nivel.index)
x = np.arange(len(niveles))
width = 0.35

colores_chatgpt = ['#e63946', '#4361ee', '#06d6a0', '#f72585', '#ffca3a', '#7209b7', '#2a9d8f', '#ff6f61']
colores_concursante = ['#f4a261', '#8ecae6', '#ffbe0b', '#bdb2ff', '#caffbf', '#b5ead7', '#ffb4a2', '#caffb9']

fig, ax = plt.subplots(figsize=(8, 5))

bars1 = ax.bar(x - width/2, [porcentaje_chatgpt.get(nivel, 0) for nivel in niveles],
               width, label='ChatGPT', color=colores_chatgpt[:len(niveles)])
bars2 = ax.bar(x + width/2, [porcentaje_concursante.get(nivel, 0) for nivel in niveles],
               width, label='Concursantes', color=colores_concursante[:len(niveles)])

# Etiquetas y formato
ax.set_xlabel('Nivel de Familiaridad')
ax.set_ylabel('Porcentaje de Aciertos (%)')
ax.set_title('Aciertos por Nivel de Familiaridad en Definiciones RAE - ChatGPT vs Concursantes')
ax.set_xticks(x)
ax.set_xticklabels(niveles)
ax.set_ylim(0, max(porcentaje_chatgpt.max(), porcentaje_concursante.max()) + 10)
ax.legend()

# Etiquetas de porcentaje
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

add_labels(bars1)
add_labels(bars2)

plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
