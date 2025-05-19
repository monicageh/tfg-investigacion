import pandas as pd
import matplotlib.pyplot as plt

# Paso 1: Cargar los datos desde los archivos JSON
try:
    roscos_df = pd.read_json('pasapalabra_questions_to_model_updated.json')
    print("Datos cargados correctamente.")
except Exception as e:
    print(f"Error al cargar los datos: {e}")
    roscos_df = pd.DataFrame()  # En caso de error, asignar un DataFrame vacío.

# Función para calcular aciertos y errores de ChatGPT y concursantes por categoría gramatical
def calcular_aciertos_errores_por_categoria(df):
    categorias = df['tipo_gramatical'].unique()
    resultados = {}
    for categoria in categorias:
        subset = df[df['tipo_gramatical'] == categoria]
        total = len(subset)
        aciertos_chatgpt = subset.apply(lambda x: x['respuesta_chatgpt'] in x['respuesta_correcta'], axis=1).sum()
        errores_chatgpt = total - aciertos_chatgpt
        aciertos_concursante = subset.apply(lambda x: x['respuesta_concursante'] in x['respuesta_correcta'], axis=1).sum()
        errores_concursante = total - aciertos_concursante
        resultados[categoria] = {
            'total': total,
            'aciertos_chatgpt': aciertos_chatgpt,
            'errores_chatgpt': errores_chatgpt,
            'aciertos_concursante': aciertos_concursante,
            'errores_concursante': errores_concursante
        }
    return resultados

# Verificar si los datos se cargaron correctamente
if not roscos_df.empty:
    # Calcular aciertos y errores por categoría gramatical
    resultados_roscos = calcular_aciertos_errores_por_categoria(roscos_df)

    print("Resultados por categoría gramatical en Roscos:\n", resultados_roscos)

    # Función para generar gráficos comparativos por categoría gramatical
    def graficar_comparacion_por_categoria(resultados, titulo):
        categorias = list(resultados.keys())
        for categoria in categorias:
            total = resultados[categoria]['total']
            aciertos_chatgpt = resultados[categoria]['aciertos_chatgpt']
            errores_chatgpt = resultados[categoria]['errores_chatgpt']
            aciertos_concursante = resultados[categoria]['aciertos_concursante']
            errores_concursante = resultados[categoria]['errores_concursante']

            fig, ax = plt.subplots(1, 2, figsize=(14, 7))
            ax[0].pie([aciertos_chatgpt, errores_chatgpt], labels=['Aciertos ChatGPT', 'Errores ChatGPT'], autopct='%1.1f%%', startangle=140)
            ax[0].set_title(f'{categoria} {titulo} - ChatGPT')

            ax[1].pie([aciertos_concursante, errores_concursante], labels=['Aciertos Concursante', 'Errores Concursante'], autopct='%1.1f%%', startangle=140)
            ax[1].set_title(f'{categoria} {titulo} - Concursante')

            plt.show()
            plt.close()  # Cerrar el gráfico actual para permitir que se generen los siguientes

    # Generar gráficos comparativos por categorías gramaticales en Pasapalabra
    print("Generando gráficos comparativos para Pasapalabra...")
    graficar_comparacion_por_categoria(resultados_roscos, 'en Pasapalabra')
else:
    print("No se cargaron datos válidos, por favor verifica el archivo JSON.")
