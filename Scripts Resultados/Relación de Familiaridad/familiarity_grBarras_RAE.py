import pandas as pd
import json
import matplotlib.pyplot as plt

# Rutas a los archivos
ruta_json = 'defsRAE_for_finetuning_model.json'
ruta_excel = 'familiarity.xlsx'

# Paso 1: Cargar el archivo JSON
with open(ruta_json, 'r', encoding='utf-8') as file:
    data_json = json.load(file)

# Extraer únicamente la primera palabra del campo 'respuesta_correcta'
palabras_json = [
    item['respuesta_correcta'].lower().strip()
    for item in data_json
    if item.get('respuesta_correcta')
]

# Paso 2: Cargar el archivo Excel
familiaridad = pd.read_excel(ruta_excel, sheet_name=0)

# Convertir nombres de columnas a minúsculas para evitar problemas
familiaridad.columns = [col.lower() for col in familiaridad.columns]

# Normalizar palabras del JSON y Excel para consistencia
familiaridad['word'] = familiaridad['word'].str.lower().str.strip()

# Paso 3: Filtrar y emparejar palabras
resultado = pd.DataFrame({
    'palabra': palabras_json,
    'familiaridad_es': [
        familiaridad.loc[familiaridad['word'] == palabra, 'gpt_dom'].iat[0]
        if palabra in familiaridad['word'].values else None
        for palabra in palabras_json
    ]
})

# Paso 4: Definir niveles de familiaridad
min_valor_es = resultado['familiaridad_es'].min(skipna=True)
max_valor_es = resultado['familiaridad_es'].max(skipna=True)

if min_valor_es is not None and max_valor_es is not None and min_valor_es >= 0 and max_valor_es <= 6.5:
    bins = [0, 1, 2, 3, 4, 5, 6, 6.5]
else:
    bins = [1, 2, 3, 4, 5, 6, 7, 8]
labels = [str(i) for i in range(1, len(bins))]

resultado['nivel'] = pd.cut(
    resultado['familiaridad_es'],
    bins=bins,
    labels=labels,
    include_lowest=True
)

# Asignar nivel '0' a palabras sin valor
resultado['nivel'] = resultado['nivel'].cat.add_categories(['0']).fillna('0')

# Paso 5: Calcular aciertos para todas las palabras del JSON
resultado['acierto'] = resultado['palabra'].apply(
    lambda w: int(any(
        w == item['respuesta_correcta'].lower().strip() and
        item['respuesta_chatgpt'].lower().strip() == w
        for item in data_json if item.get('respuesta_correcta')
    ))
)

# Paso 6: Calcular porcentajes de aciertos por nivel
aciertos_por_nivel = resultado.groupby('nivel')['acierto'].sum()
palabras_por_nivel  = resultado.groupby('nivel').size()
porcentajes_aciertos = aciertos_por_nivel / palabras_por_nivel * 100  # por nivel

# Mostrar distribución y porcentajes
print("\nDistribución por niveles de familiaridad:")
for nivel, freq in palabras_por_nivel.items():
    pct = porcentajes_aciertos[nivel]
    if nivel != '0':
        inicio = bins[labels.index(nivel)]
        fin    = bins[labels.index(nivel) + 1]
        print(f"Nivel {nivel}: {freq} palabras (rango {inicio}–{fin}) → {pct:.2f}% acierto")
    else:
        print(f"Nivel 0: {freq} palabras → {pct:.2f}% acierto")

# Paso 7: Gráfica sin '0' en el eje X
porcen_grafica = porcentajes_aciertos.drop(index='0', errors='ignore')

# Paleta solicitada
colores = [
    "#e63946",  # rojo coral fuerte
    "#4361ee",  # azul brillante
    "#06d6a0",  # verde agua vibrante
    "#f72585",  # rosa fucsia
    "#ffca3a",  # amarillo intenso
    "#7209b7",  # púrpura eléctrico
    "#2a9d8f",  # verde esmeralda
    "#ff6f61",  # salmón vibrante
    "#3a86ff",  # azul eléctrico
    "#f4a261",  # naranja cálido
    "#8338ec",  # violeta intenso
    "#4cc9f0",  # celeste vivo
    "#e76f51",  # ladrillo suave
    "#8ecae6",  # azul claro pero saturado
    "#ffbe0b",  # mostaza viva
]

plt.figure(figsize=(5, 4))
bars = plt.bar(
    porcen_grafica.index,
    porcen_grafica.values,
    color=colores[:len(porcen_grafica)],
    width=0.75
)
for bar in bars:
    h = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        h + 1,
        f'{h:.1f}%',
        ha='center',
        va='bottom',
        fontsize=8
    )
plt.ylim(0, porcen_grafica.max() + 10)
plt.title('Aciertos por Nivel de Familiaridad en RAE - ChatGPT-4o', fontsize=11)
plt.xlabel('Nivel de Familiaridad')
plt.ylabel('Porcentaje de Aciertos (%)')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
