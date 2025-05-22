import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np

# Rutas a los archivos
ruta_json = 'pasapalabra_questions_to_model_gramatical.json'
ruta_excel = 'familiarity.xlsx'

# Paso 1: Cargar el archivo JSON
with open(ruta_json, 'r', encoding='utf-8') as file:
    data_json = json.load(file)

# Paso 2: Extraer palabras del JSON (respuesta_correcta como lista plana)
palabras_json = []
for item in data_json:
    if item.get('respuesta_correcta'):
        for palabra in item['respuesta_correcta']:
            palabras_json.append(palabra.lower().strip())

# Paso 3: Cargar el archivo Excel y normalizar
familiaridad = pd.read_excel(ruta_excel, sheet_name=0)
familiaridad.columns = [col.lower() for col in familiaridad.columns]
familiaridad['word'] = familiaridad['word'].str.lower().str.strip()

# Paso 4: Crear DataFrame de emparejamiento
resultado = pd.DataFrame({
    'palabra': palabras_json,
    'familiaridad_es': [
        familiaridad.loc[familiaridad['word'] == palabra, 'gpt_dom'].iat[0]
        if palabra in familiaridad['word'].values else None
        for palabra in palabras_json
    ]
})

# Paso 5: Definir niveles de familiaridad
min_val = resultado['familiaridad_es'].min(skipna=True)
max_val = resultado['familiaridad_es'].max(skipna=True)
if min_val is not None and max_val is not None and min_val >= 0 and max_val <= 6.5:
    bins = [0, 1, 2, 3, 4, 5, 6, 6.5]
else:
    bins = [1, 2, 3, 4, 5, 6, 7, 8]
labels = [f'Nivel {i}' for i in range(1, len(bins))]

resultado['nivel'] = pd.cut(
    resultado['familiaridad_es'],
    bins=bins,
    labels=labels,
    include_lowest=True
)

# Paso 6: Filtrar solo filas con nivel asignado
resultado = resultado[resultado['nivel'].notna()]

# Paso 7: Calcular aciertos por nivel para ChatGPT y concursante
resultado['acierto_chatgpt'] = resultado['palabra'].apply(
    lambda w: int(any(
        w == correcta.lower().strip()
        for item in data_json if item.get('respuesta_correcta')
        for correcta in item['respuesta_correcta']
        if item['respuesta_chatgpt'].lower().strip() == w
    ))
)
resultado['acierto_concursante'] = resultado['palabra'].apply(
    lambda w: int(any(
        w == correcta.lower().strip()
        for item in data_json if item.get('respuesta_correcta')
        for correcta in item['respuesta_correcta']
        if item['respuesta_concursante'].lower().strip() == w
    ))
)

# Paso 8: Calcular porcentajes de acierto por nivel
aciertos_chatgpt = resultado.groupby('nivel')['acierto_chatgpt'].sum()
palabras_nivel = resultado.groupby('nivel').size()
porcentajes_chatgpt = (aciertos_chatgpt / palabras_nivel) * 100

aciertos_conc = resultado.groupby('nivel')['acierto_concursante'].sum()
porcentajes_conc = (aciertos_conc / palabras_nivel) * 100

# Mostrar porcentajes en consola
print("Porcentajes de acierto por nivel:")
for nivel in labels:
    pct_gpt = porcentajes_chatgpt.get(nivel, 0)
    pct_con = porcentajes_conc.get(nivel, 0)
    print(f"{nivel}: ChatGPT {pct_gpt:.2f}%, Concursante {pct_con:.2f}%")

# Paso 9: Visualización comparativa
niveles = labels
x = np.arange(len(niveles))
width = 0.35

fig, ax = plt.subplots(figsize=(9, 5))
color_chatgpt = 'steelblue'
color_conc = 'salmon'

bars1 = ax.bar(x - width/2, [porcentajes_chatgpt.get(n, 0) for n in niveles],
               width, label='ChatGPT', color=color_chatgpt)
bars2 = ax.bar(x + width/2, [porcentajes_conc.get(n, 0) for n in niveles],
               width, label='Concursantes', color=color_conc)

ax.set_xlabel('Nivel de Familiaridad')
ax.set_ylabel('Porcentaje de Aciertos (%)')
ax.set_title('Aciertos por Nivel de Familiaridad en Pasapalabra - CHATGPT-3.5 vs Concursantes')
ax.set_xticks(x)
ax.set_xticklabels(niveles)
ax.set_ylim(0, max(porcentajes_chatgpt.max(), porcentajes_conc.max()) + 10)
ax.legend()

# Añadir etiquetas de porcentaje
for bar in list(bars1) + list(bars2):
    h = bar.get_height()
    ax.annotate(f'{h:.1f}%',
                xy=(bar.get_x() + bar.get_width()/2, h),
                xytext=(0, 3), textcoords='offset points',
                ha='center', va='bottom', fontsize=8)

plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()