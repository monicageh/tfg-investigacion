import pandas as pd
import json
import matplotlib.pyplot as plt

# Rutas a los archivos
ruta_json = 'pasapalabra_questions_to_model_gramatical.json'
ruta_excel = 'familiarity.xlsx'

# Paso 1: Cargar el archivo JSON
with open(ruta_json, 'r', encoding='utf-8') as file:
    data_json = json.load(file)

# Obtener el número total de palabras como el ID del último objeto en el JSON
total_palabras = int(data_json[-1]['id'])

# Paso 2: Extraer palabras del JSON (respuesta_correcta como lista plana)
palabras_json = [palabra.lower().strip()
                 for item in data_json if item.get('respuesta_correcta')
                 for palabra in item['respuesta_correcta']]

# Paso 3: Cargar el archivo Excel
familiaridad = pd.read_excel(ruta_excel, sheet_name=0)

# Convertir nombres de columnas a minúsculas para evitar problemas
familiaridad.columns = [col.lower() for col in familiaridad.columns]

# Normalizar palabras del JSON y Excel para consistencia
familiaridad['word'] = familiaridad['word'].str.lower().str.strip()

# Paso 4: Filtrar y emparejar palabras
coincidencias = familiaridad[familiaridad['word'].isin(palabras_json)]

# Crear DataFrame de las palabras emparejadas con familiaridad
resultado = pd.DataFrame({
    'palabra': palabras_json,
    'familiaridad_es': [familiaridad.loc[familiaridad['word'] == palabra, 'gpt_dom'].iloc[0]
                        if palabra in familiaridad['word'].values else None
                        for palabra in palabras_json]
})

# Verificar el rango de valores en gpt_dom para ajustar los niveles
min_valor_es = resultado['familiaridad_es'].min(skipna=True)
max_valor_es = resultado['familiaridad_es'].max(skipna=True)

print(f"Rango de familiaridad en español (gpt_dom): Min: {min_valor_es}, Max: {max_valor_es}")

# Ajustar los niveles según el rango de los valores
if min_valor_es is not None and max_valor_es is not None and min_valor_es >= 0 and max_valor_es <= 6.5:
    bins = [0, 1, 2, 3, 4, 5, 6, 6.5]
    labels = ['Nivel 1', 'Nivel 2', 'Nivel 3', 'Nivel 4', 'Nivel 5', 'Nivel 6', 'Nivel 7']
else:
    bins = [1, 2, 3, 4, 5, 6, 7, 8]
    labels = ['Nivel 1', 'Nivel 2', 'Nivel 3', 'Nivel 4', 'Nivel 5', 'Nivel 6', 'Nivel 7']

# Clasificar palabras por los niveles de familiaridad para las que tienen valores
resultado['nivel'] = pd.cut(
    resultado['familiaridad_es'], 
    bins=bins, 
    labels=labels, 
    include_lowest=True
)

# Asignar "Nivel 0" a las palabras sin familiaridad
resultado['nivel'] = resultado['nivel'].cat.add_categories(['Nivel 0']).fillna('Nivel 0')

# Paso 5: Calcular aciertos para ChatGPT y concursante
# Comparar respuesta_chatgpt y respuesta_concursante con cada palabra del array respuesta_correcta
resultado['acierto_chatgpt'] = resultado['palabra'].apply(
    lambda palabra: 1 if any(
        palabra == correcta.lower().strip()
        for item in data_json if item.get('respuesta_correcta')
        for correcta in item['respuesta_correcta']
        if item['respuesta_chatgpt'].lower().strip() == palabra
    ) else 0
)

resultado['acierto_concursante'] = resultado['palabra'].apply(
    lambda palabra: 1 if any(
        palabra == correcta.lower().strip()
        for item in data_json if item.get('respuesta_correcta')
        for correcta in item['respuesta_correcta']
        if item['respuesta_concursante'].lower().strip() == palabra
    ) else 0
)

# Paso 6: Calcular porcentajes de aciertos por nivel
aciertos_por_nivel_chatgpt = resultado.groupby('nivel')['acierto_chatgpt'].sum()
aciertos_por_nivel_concursante = resultado.groupby('nivel')['acierto_concursante'].sum()
palabras_por_nivel = resultado.groupby('nivel').size()

porcentajes_aciertos_chatgpt = (aciertos_por_nivel_chatgpt / palabras_por_nivel) * 100
porcentajes_aciertos_concursante = (aciertos_por_nivel_concursante / palabras_por_nivel) * 100

# Imprimir los totales y rangos de cada nivel
print("\nDistribución por niveles de familiaridad:")
for nivel, frecuencia in palabras_por_nivel.items():
    if nivel != "Nivel 0":
        rango_inicio = bins[labels.index(nivel)]
        rango_fin = bins[labels.index(nivel) + 1]
        print(f"{nivel}: {frecuencia} palabras - Rango: {rango_inicio} a {rango_fin} - "
              f"Aciertos ChatGPT: {porcentajes_aciertos_chatgpt[nivel]:.2f}%, "
              f"Aciertos Concursante: {porcentajes_aciertos_concursante[nivel]:.2f}%")
    else:
        print(f"{nivel}: {frecuencia} palabras - "
              f"Aciertos ChatGPT: {porcentajes_aciertos_chatgpt[nivel]:.2f}%, "
              f"Aciertos Concursante: {porcentajes_aciertos_concursante[nivel]:.2f}%")

import numpy as np

# Paso 7: Crear gráfico de barras comparativo
niveles = list(palabras_por_nivel.index)
x = np.arange(len(niveles))  # posición de cada grupo en el eje x
width = 0.35  # ancho de las barras

# Paleta pastel y fuerte por pareja
colores_chatgpt = ['#ff6666', '#3399ff', '#66cc66', '#ff9933', '#9966cc', '#ff66b2', '#33cccc', '#999999']
colores_concursante = ['#ffb3b3', '#99ccff', '#b3ffb3', '#ffd699', '#dab6ff', '#ffb3d9', '#a6f2f2', '#d9d9d9']

fig, ax = plt.subplots(figsize=(9, 5))

# Crear las barras
bars1 = ax.bar(x - width/2, [porcentajes_aciertos_chatgpt.get(nivel, 0) for nivel in niveles],
               width, label='ChatGPT', color=colores_chatgpt[:len(niveles)])
bars2 = ax.bar(x + width/2, [porcentajes_aciertos_concursante.get(nivel, 0) for nivel in niveles],
               width, label='Concursantes', color=colores_concursante[:len(niveles)])

# Etiquetas
ax.set_xlabel('Nivel de Familiaridad')
ax.set_ylabel('Porcentaje de Aciertos (%)')
ax.set_title('Aciertos por Nivel de Familiaridad en ROSCOS - CHATGPT-3.5')
ax.set_xticks(x)
ax.set_xticklabels(niveles)
ax.set_ylim(0, max(porcentajes_aciertos_chatgpt.max(), porcentajes_aciertos_concursante.max()) + 10)
ax.legend()

# Añadir etiquetas de porcentaje en cada barra
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
