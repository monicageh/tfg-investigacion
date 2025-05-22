import pandas as pd
import json
import matplotlib.pyplot as plt

# Rutas a los archivos
ruta_json = 'defsIngles_for_finetuning_model copy.json'
ruta_excel = 'familiarity.xlsx'

# Paso 1: Cargar el archivo JSON
with open(ruta_json, 'r', encoding='utf-8') as file:
    data_json = json.load(file)

# Paso 2: Extraer palabras del JSON (respuesta_correcta como lista)
palabras_json = []
for item in data_json:
    if item.get('respuesta_correcta'):
        palabra = item['respuesta_correcta'].lower().strip()
        palabras_json.append(palabra)

# Paso 3: Cargar Excel y normalizar
familiaridad = pd.read_excel(ruta_excel, sheet_name=0)
familiaridad.columns = [col.lower() for col in familiaridad.columns]
familiaridad['word'] = familiaridad['word'].str.lower().str.strip()

# Crear DataFrame con familiaridad
resultado = pd.DataFrame({
    'palabra': palabras_json,
    'familiaridad_en': [
        familiaridad.loc[familiaridad['word']==p, 'gpt_dom'].iat[0]
        if p in familiaridad['word'].values else None
        for p in palabras_json
    ]
})

# Paso 4: Definir niveles según rango
min_val = resultado['familiaridad_en'].min(skipna=True)
max_val = resultado['familiaridad_en'].max(skipna=True)
if min_val is not None and max_val is not None and min_val>=0 and max_val<=6.5:
    bins = [0,1,2,3,4,5,6,6.5]
else:
    bins = [1,2,3,4,5,6,7,8]
labels = [str(i) for i in range(1, len(bins))]

resultado['nivel'] = pd.cut(
    resultado['familiaridad_en'], bins=bins,
    labels=labels, include_lowest=True
)
# Asignar nivel 0 a NaN
iresultado = resultado
resultado['nivel'] = resultado['nivel'].cat.add_categories(['0']).fillna('0')

# Paso 5: Calcular aciertos por nivel
resultado['acierto'] = resultado['palabra'].apply(
    lambda w: int(any(
        w == item['respuesta_correcta'].lower().strip() and
        item['respuesta_chatgpt'].lower().strip() == w
        for item in data_json if item.get('respuesta_correcta')
    ))
)

# Paso 6: Porcentajes por nivel
aciertos = resultado.groupby('nivel')['acierto'].sum()
totales = resultado.groupby('nivel').size()
porcentajes = aciertos / totales * 100

# Mostrar resultados
print("Porcentajes de acierto por nivel:")
for lvl in labels:
    print(f"Nivel {lvl}: {porcentajes.get(lvl,0):.2f}%")
print(f"Nivel 0: {porcentajes.get('0',0):.2f}%")

# Paso 7: Gráfica
por_graf = porcentajes.drop(index='0', errors='ignore')

colores = [
    "#e63946","#4361ee","#06d6a0","#f72585","#ffca3a",
    "#7209b7","#2a9d8f","#ff6f61","#3a86ff","#f4a261",
    "#8338ec","#4cc9f0","#e76f51","#8ecae6","#ffbe0b"
]

plt.figure(figsize=(5,4))
bars = plt.bar(
    por_graf.index, por_graf.values,
    color=colores[:len(por_graf)], width=0.75
)
for bar in bars:
    h = bar.get_height()
    plt.text(
        bar.get_x()+bar.get_width()/2, h+1,
        f"{h:.1f}%", ha='center', va='bottom', fontsize=8
    )
plt.ylim(0, por_graf.max()+10)
plt.title('Aciertos por Nivel de Familiaridad en Inglés - CHATGPT-4o', fontsize=11)
plt.xlabel('Nivel de Familiaridad')
plt.ylabel('Porcentaje de Aciertos (%)')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

