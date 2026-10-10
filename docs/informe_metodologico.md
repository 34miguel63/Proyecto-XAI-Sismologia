Informe metodológico: explicabilidad de un modelo de IA aplicado a señales sísmicas

1. Introducción

La Inteligencia Artificial permite desarrollar modelos capaces de identificar patrones en datos complejos. En el análisis sísmico, estos modelos pueden estudiarse para clasificar señales y distinguir patrones que podrían corresponder a eventos sísmicos o a ruido.

Sin embargo, conocer únicamente la predicción de un modelo no permite entender qué información influyó en ella. La Inteligencia Artificial Explicable (XAI) agrupa métodos que ayudan a interpretar el comportamiento de los modelos.

Este trabajo aplica Integrated Gradients a una red neuronal convolucional unidimensional entrenada con señales sintéticas. También incorpora herramientas para descargar y analizar registros sísmicos reales como preparación para futuras pruebas.

2. Objetivo

Aplicar un método XAI para analizar las regiones de una señal que contribuyen a las predicciones de un modelo de clasificación basado en una CNN 1D.

3. Generación de datos

Se implementó un generador de 1000 señales sintéticas de 500 muestras cada una. El conjunto incluye 500 señales de ruido y 500 señales que simulan eventos mediante componentes sinusoidales y una envolvente de amplitud decreciente.

Las señales se normalizaron antes de utilizarlas en el entrenamiento.

Este procedimiento permite controlar las características de los datos y probar el flujo de trabajo. No obstante, las señales generadas artificialmente no reproducen toda la complejidad de los registros sísmicos naturales.

4. Arquitectura del modelo

Se desarrolló una red neuronal convolucional unidimensional con capas convolucionales, funciones de activación, reducción de dimensionalidad y capas finales de clasificación.

La red recibe una señal como entrada y produce puntuaciones que se convierten en probabilidades para las clases definidas: ruido y evento sintético.

Los datos se dividieron en entrenamiento y prueba mediante una partición estratificada, de forma que ambas clases estuvieran representadas en los conjuntos.

5. Evaluación del modelo

En la ejecución documentada se obtuvo:

- Exactitud: 1,00.
- F1: 1,00.
- Clasificaciones correctas registradas: 100 de 100 para cada clase del conjunto de prueba.

Estos resultados corresponden al conjunto sintético empleado. No deben interpretarse como evidencia de una exactitud equivalente en terremotos reales.

6. Método de explicabilidad: Integrated Gradients

Integrated Gradients atribuye contribuciones a las características de entrada a partir de los gradientes del modelo, integrados a lo largo de una trayectoria entre una línea base y la entrada analizada.

En este proyecto se utilizó Captum, con una línea base de ceros y 100 pasos de integración. Se seleccionó como objetivo la clase de evento sintético para estudiar la contribución de las distintas muestras de una señal.

En el ejemplo documentado, el modelo asignó aproximadamente las siguientes probabilidades:

- Ruido: 0,0030.
- Evento sintético: 0,9970.

La diferencia de convergencia registrada fue aproximadamente 0,000752.

Las atribuciones permiten visualizar qué regiones de la señal contribuyeron a la salida seleccionada. El resultado depende del modelo, la entrada, la clase objetivo y la línea base elegida. Por ello, una atribución no debe interpretarse como una prueba causal ni como confirmación independiente de que ocurrió un terremoto.

7. Adquisición y análisis de señales reales

Se prepararon scripts para descargar registros sísmicos mediante servicios de datos sísmicos y guardarlos en formato MiniSEED. También se implementaron herramientas para leer los registros, obtener metadatos, calcular estadísticas, representar las formas de onda y aplicar filtrado cuando la frecuencia de muestreo lo permite.

Se añadió una consulta al catálogo del USGS para obtener información de eventos sísmicos de una fecha determinada.

Estas actividades demuestran que se dispone de un flujo inicial para obtener y explorar registros reales. Sin embargo, no se debe asociar automáticamente un registro con un evento del catálogo solo porque coincidan las fechas. Para confirmar esa relación es necesario comprobar los tiempos de origen, la ubicación del evento, la estación, la fase sísmica esperada y las características del registro.

8. Limitaciones experimentales

La principal limitación es que el clasificador se entrenó con datos sintéticos. El análisis de registros reales todavía no equivale a una evaluación de rendimiento del modelo con ejemplos reales etiquetados.

Entre las limitaciones se encuentran:

1. Las señales sintéticas no abarcan la diversidad de los terremotos naturales.
2. No se ha demostrado que el modelo generalice a estaciones, regiones y condiciones instrumentales distintas.
3. Una probabilidad alta del modelo no garantiza que la clasificación sea correcta.
4. Integrated Gradients explica la dependencia de la predicción respecto de la entrada, pero no verifica por sí solo la validez física de la predicción.
5. Una evaluación real requiere etiquetas verificadas y una separación de datos que evite fugas entre entrenamiento y prueba.

9. Trabajo futuro

Para continuar el proyecto se propone:

1. Obtener registros reales de eventos sísmicos y de ruido con metadatos verificables.
2. Preparar las señales con un procedimiento reproducible y documentado.
3. Establecer etiquetas basadas en fuentes fiables.
4. Separar los datos por evento, estación o intervalo temporal cuando corresponda, evitando que fragmentos relacionados aparezcan en entrenamiento y prueba.
5. Entrenar o ajustar el modelo con los datos reales.
6. Evaluar exactitud, precisión, exhaustividad, F1, matriz de confusión y tasas de falsos positivos y falsos negativos.
7. Aplicar Integrated Gradients a ejemplos reales del conjunto de prueba.
8. Comparar las explicaciones con las características conocidas de las señales y documentar los casos de error.

10. Conclusiones

El trabajo implementa una CNN 1D y aplica Integrated Gradients para explicar predicciones sobre señales sísmicas sintéticas. También incorpora herramientas de adquisición, visualización y análisis de registros reales.

Por tanto, el proyecto constituye una demostración práctica de un método XAI aplicado a un problema de clasificación de señales. La validación de la capacidad del modelo para detectar terremotos reales queda como una etapa posterior que requiere datos reales etiquetados y una evaluación experimental independiente.

Referencias

- Sundararajan, M., Taly, A. y Yan, Q. (2017). Axiomatic Attribution for Deep Networks. Proceedings of the 34th International Conference on Machine Learning.
- Captum: https://captum.ai/docs/
- PyTorch: https://pytorch.org/docs/
- ObsPy: https://docs.obspy.org/
- USGS Earthquake Catalog: https://earthquake.usgs.gov/earthquakes/search/
