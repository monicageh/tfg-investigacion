import pandas as pd
import matplotlib.pyplot as plt

# Paso 1: Cargar los datos desde los archivos JSON
roscos_df = pd.read_json('pasapalabra_questions_to_model_updated.json')
rae_df = pd.read_json('defsRAE_for_finetuning_model_updated.json')
ingles_df = pd.read_json('defsIngles_for_finetuning_model_updated.json')

# Función para calcular la tasa de aciertos en bruto
def calcular_tasa_aciertos(df):
    aciertos = sum(
        x['respuesta_chatgpt'] in x['respuesta_correcta'] 
        for _, x in df.iterrows()
    )
    total = len(df)
    tasa_aciertos = aciertos / total if total > 0 else 0
    return tasa_aciertos

# Calcular tasa de aciertos en bruto
tasa_aciertos_roscos = calcular_tasa_aciertos(roscos_df)
tasa_aciertos_rae = calcular_tasa_aciertos(rae_df)
tasa_aciertos_ingles = calcular_tasa_aciertos(ingles_df)

print("Tasa de aciertos en Roscos:", tasa_aciertos_roscos)
print("Tasa de aciertos en RAE:", tasa_aciertos_rae)
print("Tasa de aciertos en Inglés:", tasa_aciertos_ingles)

# Función para calcular aciertos y totales por categoría gramatical
def calcular_aciertos_y_totales_por_categoria(df):
    categorias = ['sustantivo', 'verbo', 'adjetivo']  # Orden deseado
    resultados = {cat: {'total': 0, 'aciertos': 0} for cat in categorias}  # Inicializar con 0
    for categoria in categorias:
        subset = df[df['tipo_gramatical'] == categoria]
        total = len(subset)
        aciertos = sum(
            x['respuesta_chatgpt'] in x['respuesta_correcta'] 
            for _, x in subset.iterrows()
        )
        resultados[categoria] = {'total': total, 'aciertos': aciertos}  # Aciertos como enteros
    return resultados

# Calcular aciertos y totales por categoría gramatical
resultados_roscos = calcular_aciertos_y_totales_por_categoria(roscos_df)
resultados_rae = calcular_aciertos_y_totales_por_categoria(rae_df)
resultados_ingles = calcular_aciertos_y_totales_por_categoria(ingles_df)

print("Resultados por categoría gramatical en Roscos:\n", resultados_roscos)
print("Resultados por categoría gramatical en RAE:\n", resultados_rae)
print("Resultados por categoría gramatical en Inglés:\n", resultados_ingles)

# Generar gráficas para visualizar los resultados
def graficar_resultados(resultados, titulo):
    categorias = ['sustantivo', 'verbo', 'adjetivo']  # Orden fijo
    totales = [resultados[cat]['total'] for cat in categorias]
    aciertos = [resultados[cat]['aciertos'] for cat in categorias]
    
    x = range(len(categorias))
    
    # Colores para las barras de cada categoría
    colores_totales = ['#ff9999', '#3399ff', '#99ff99']  # Más contraste en azul claro
    colores_aciertos = ['#ff6666', '#003f88', '#33cc66']  # Azul oscuro más intenso
    
    # Dibujar barras
    plt.bar(x, totales, width=0.4, color=colores_totales, align='center')
    plt.bar(x, aciertos, width=0.4, color=colores_aciertos, align='edge')
    
    # Configuración de la gráfica
    plt.xlabel('Categoría Gramatical')
    plt.ylabel('Cantidad')
    plt.title(titulo)
    plt.xticks(x, categorias, rotation=0)  # Etiquetas horizontales
    
    # Crear leyenda completa con orden solicitado
    legend_labels = [
        'Total (sustantivo)', 'Aciertos (sustantivo)',
        'Total (verbo)', 'Aciertos (verbo)',
        'Total (adjetivo)', 'Aciertos (adjetivo)'
    ]
    legend_colors = [
        colores_totales[0], colores_aciertos[0],  # Sustantivo
        colores_totales[1], colores_aciertos[1],  # Verbo
        colores_totales[2], colores_aciertos[2],  # Adjetivo
    ]
    plt.legend(
        handles=[plt.Rectangle((0, 0), 1, 1, color=color) for color in legend_colors],
        labels=legend_labels,
        loc='upper right',
        title='Leyenda',
        fontsize='small',
        title_fontsize='medium'
    )
    
    plt.tight_layout()  # Ajustar el espacio para evitar solapamiento
    plt.show()

graficar_resultados(resultados_roscos, 'Resultados por Categoría Gramatical en Roscos')
graficar_resultados(resultados_rae, 'Resultados por Categoría Gramatical en RAE')
graficar_resultados(resultados_ingles, 'Resultados por Categoría Gramatical en Inglés')
