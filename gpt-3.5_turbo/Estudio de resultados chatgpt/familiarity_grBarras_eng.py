import pandas as pd
import json
import matplotlib.pyplot as plt

# Rutas a los archivos
ruta_json = 'defsIngles_questions_to_model_gramatical.json' 
ruta_excel = 'familiarity.xlsx'

# Paso 1: Cargar el archivo JSON
with open(ruta_json, 'r', encoding='utf-8') as file:
    data_json = json.load(file)

# Extraer únicamente la primera palabra del campo 'respuesta_correcta'
palabras_json = [item['respuesta_correcta'].lower().strip() for item in data_json if item.get('respuesta_correcta')]

# Paso 2: Cargar el archivo Excel
familiaridad = pd.read_excel(ruta_excel, sheet_name=0)

# Convertir nombres de columnas a minúsculas para evitar problemas
familiaridad.columns = [col.lower() for col in familiaridad.columns]

# Normalizar palabras del JSON y Excel para consistencia
familiaridad['word'] = familiaridad['word'].str.lower().str.strip()

# Paso 3: Filtrar y emparejar palabras
coincidencias = familiaridad[familiaridad['word'].isin(palabras_json)]

# Crear DataFrame de las palabras emparejadas con familiaridad
resultado = pd.DataFrame({
    'palabra': palabras_json,
    'familiaridad_en': [familiaridad.loc[familiaridad['word'] == palabra, 'gpt_dom'].iloc[0]
                        if palabra in familiaridad['word'].values else None
                        for palabra in palabras_json]
})

# Paso 4: Verificar el rango de valores en gpt_dom para ajustar los niveles
min_valor_es = resultado['familiaridad_en'].min(skipna=True)
max_valor_es = resultado['familiaridad_en'].max(skipna=True)

print(f"Rango de familiaridad en español (gpt_dom): Min: {min_valor_es}, Max: {max_valor_es}")

# Ajustar los niveles según el rango de los valores
if min_valor_es is not None and max_valor_es is not None and min_valor_es >= 0 and max_valor_es <= 6.5:
    bins = [0, 1, 2, 3, 4, 5, 6, 6.5]
    labels = ['1', '2', '3', '4', '5', '6', '7']
else:
    bins = [1, 2, 3, 4, 5, 6, 7, 8]
    labels = ['1', '2', '3', '4', '5', '6', '7']

# Clasificar palabras por los niveles de familiaridad para las que tienen valores
resultado['nivel'] = pd.cut(
    resultado['familiaridad_en'], 
    bins=bins, 
    labels=labels, 
    include_lowest=True
)

# Asignar "Nivel 0" a las palabras sin familiaridad
resultado['nivel'] = resultado['nivel'].cat.add_categories(['0']).fillna('0')

# Contar la frecuencia de cada nivel
frecuencias = resultado['nivel'].value_counts()

# Filtrar niveles con frecuencia > 0
frecuencias = frecuencias[frecuencias > 0]

# Paso 5: Calcular aciertos para todas las palabras del JSON
resultado['acierto'] = resultado['palabra'].apply(
    lambda palabra: 1 if any(
        palabra == item['respuesta_correcta'].lower().strip() 
        for item in data_json 
        if item.get('respuesta_correcta') and item['respuesta_chatgpt'].lower().strip() == palabra
    ) else 0
)

# Calcular los porcentajes de aciertos por nivel
aciertos_por_nivel = resultado.groupby('nivel')['acierto'].sum()
palabras_por_nivel = resultado.groupby('nivel').size()
porcentajes_aciertos = (aciertos_por_nivel / palabras_por_nivel) * 100

# Imprimir los totales y rangos de cada nivel
total_palabras = len(data_json)
print("\nDistribución por niveles de familiaridad:")
for nivel, frecuencia in palabras_por_nivel.items():
    if nivel != "0":
        rango_inicio = bins[labels.index(nivel)]
        rango_fin = bins[labels.index(nivel) + 1]
        print(f"{nivel}: {frecuencia} palabras - Rango: {rango_inicio} a {rango_fin} - Aciertos: {porcentajes_aciertos[nivel]:.2f}%")
    else:
        print(f"{nivel}: {frecuencia} palabras - Aciertos: {porcentajes_aciertos[nivel]:.2f}%")

# Paso 6: Crear gráfico de barras más compacto y con eje X estrecho

import matplotlib.pyplot as plt

# Paleta pastel personalizada inspirada en tu imagen
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


# Filtrar niveles con datos válidos
porcentajes_validos = porcentajes_aciertos.dropna()

# Crear figura más compacta
plt.figure(figsize=(5, 4))  # Tamaño más pequeño

# Gráfico de barras con barras más estrechas
bars = plt.bar(
    porcentajes_validos.index,
    porcentajes_validos.values,
    color=colores[:len(porcentajes_validos)],
    width=0.75  # Barra más estrecha
)

# Añadir etiquetas de porcentaje
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2, 
        height + 1,
        f'{height:.1f}%', 
        ha='center', 
        va='bottom',
        fontsize=8
    )

# Escala dinámica del eje Y
max_val = porcentajes_validos.max()
plt.ylim(0, max_val + 10)

# Personalización general
plt.title('Aciertos por Nivel de Familiaridad en Inglés - CHATGPT-3.5 ', fontsize=11)
plt.xlabel('Nivel de Familiaridad')
plt.ylabel('Porcentaje de Aciertos (%)')
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Menos espacio alrededor
plt.tight_layout()

# Mostrar
plt.show()
