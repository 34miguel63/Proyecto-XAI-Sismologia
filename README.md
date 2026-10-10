XAI aplicado a señales sísmicas

1. Descripción del proyecto

Este proyecto estudia el uso de métodos de Inteligencia Artificial Explicable (XAI, por sus siglas en inglés) para interpretar las predicciones de un modelo de aprendizaje automático aplicado al análisis de señales sísmicas.

Se implementó una red neuronal convolucional unidimensional (CNN 1D) en Python para clasificar señales sintéticas en dos categorías: ruido y evento sísmico sintético. Posteriormente, se aplicó el método Integrated Gradients, utilizando la biblioteca Captum, para identificar qué regiones de las señales contribuyen a las predicciones del modelo.

Además, se desarrollaron herramientas para descargar, visualizar y analizar registros sísmicos reales, así como para consultar un catálogo de eventos sísmicos.

2. Objetivo general

Aplicar un método de Inteligencia Artificial Explicable para interpretar las predicciones de un modelo de IA destinado a la clasificación de señales sísmicas y estudiar su posible aplicación al análisis de registros reales.

3. Objetivos específicos

- Generar señales sintéticas representativas de ruido y eventos sísmicos simulados.
- Construir y entrenar una red neuronal convolucional para clasificar las señales.
- Evaluar el rendimiento del modelo con datos de prueba.
- Aplicar Integrated Gradients para estudiar las regiones de la señal que influyen en las predicciones.
- Obtener y analizar registros sísmicos reales.
- Documentar las limitaciones del experimento y los pasos necesarios para validar el modelo con datos reales etiquetados.

4. Tecnologías utilizadas

- Python 3.
- PyTorch para construir y entrenar la red neuronal.
- Captum para aplicar Integrated Gradients.
- NumPy y SciPy para el procesamiento numérico.
- Matplotlib para visualizar las señales y los resultados.
- Scikit-learn para evaluar el clasificador.
- ObsPy para trabajar con registros sísmicos en formato MiniSEED.
- Pandas y Requests para gestionar datos y realizar consultas.

5. Metodología

5.1. Generación de datos sintéticos

Se creó un conjunto de 1000 señales sintéticas de longitud 500 muestras: 500 correspondientes a ruido y 500 a eventos simulados. Las señales se normalizaron para facilitar su procesamiento.

Estas señales permiten desarrollar y probar el procedimiento experimental, pero no sustituyen a un conjunto de registros sísmicos reales con etiquetas verificadas.

5.2. Entrenamiento del modelo

Se implementó una CNN 1D que procesa las señales y produce una clasificación entre las dos categorías definidas. Los datos se dividieron en conjuntos de entrenamiento y prueba.

En la ejecución documentada se obtuvo una exactitud de 1,00 y un F1 de 1,00 en el conjunto de prueba sintético. Estos valores describen únicamente ese experimento y no demuestran que el modelo pueda detectar terremotos reales con la misma precisión.

5.3. Explicabilidad con Integrated Gradients

Integrated Gradients permite atribuir a las distintas partes de una entrada una contribución relativa a la predicción del modelo. En este proyecto se utilizó Captum con una línea base de ceros y 100 pasos de integración.

En una señal sintética clasificada como evento, el modelo asignó aproximadamente un 99,7 % de probabilidad a esa categoría. Las atribuciones mostraron qué regiones de la señal contribuyeron a la predicción.

La explicación permite inspeccionar el comportamiento del modelo, pero no demuestra por sí sola que la predicción sea correcta ni que las regiones destacadas sean causas físicas del terremoto.

5.4. Análisis de registros reales

Se desarrollaron scripts para descargar señales sísmicas, leer registros MiniSEED, calcular estadísticas, visualizar formas de onda y aplicar un filtrado cuando corresponde. También se creó un script para consultar el catálogo sísmico del USGS.

Este análisis sirve como preparación para una evaluación con datos reales. La descarga de un registro y la consulta de un catálogo no bastan, por sí solas, para confirmar que el registro corresponde a la llegada de un terremoto concreto ni para validar el clasificador.

6. Resultados obtenidos

- Se generaron señales sintéticas para dos clases.
- Se entrenó una CNN 1D.
- Se obtuvieron una exactitud de 1,00 y un F1 de 1,00 en la prueba sintética documentada.
- Se aplicó Integrated Gradients a una señal sintética.
- Se descargaron y analizaron registros sísmicos reales.
- Se generaron gráficas y archivos de resultados para apoyar el análisis.

7. Limitaciones

El modelo se entrenó con señales sintéticas. Por tanto, los resultados actuales no constituyen una validación de detección de terremotos reales.

Para comprobar esa capacidad será necesario preparar un conjunto de señales reales etiquetadas y verificadas, incluir tanto eventos sísmicos como ruido, separar correctamente los datos de entrenamiento y prueba y evaluar el modelo con métricas como precisión, exhaustividad, F1 y matriz de confusión. También será necesario aplicar el método XAI a ejemplos reales de prueba.

8. Estructura del proyecto

La estructura puede variar según los archivos presentes en el entorno local:

Proyecto XAI Sismologia/
├── README.md
├── requirements.txt
├── .gitignore
├── generar_datos.py
├── entrenar_cnn.py
├── explicar_modelo.py
├── descargar_senal_real.py
├── descargar_senal_evento.py
├── analizar_senal_real.py
├── analizar_evento_real.py
├── consultar_catalogo.py
├── inspeccionar_stead.py
├── preparar_datos_stead.py
├── docs/
│   └── informe_metodologico.md
├── datos/
├── modelos/
└── resultados/

9. Instalación y ejecución

Se recomienda utilizar Python 3.12 y un entorno virtual.

En PowerShell, desde la carpeta del proyecto:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

Para ejecutar el experimento sintético:

python generar_datos.py
python entrenar_cnn.py
python explicar_modelo.py

Los scripts de descarga y análisis de señales reales son complementarios y deben ejecutarse después de comprobar su configuración y disponibilidad de conexión a Internet.

10. Conclusión

El proyecto demuestra la aplicación de un método XAI para interpretar las predicciones de una red neuronal convolucional sobre señales sísmicas sintéticas. Integrated Gradients proporciona información sobre las regiones de la señal que influyen en la salida del modelo y facilita el análisis de su comportamiento.

El trabajo también incorpora herramientas para inspeccionar registros reales y consultar catálogos sísmicos. Sin embargo, la capacidad de detectar terremotos reales de forma fiable queda pendiente de una validación específica con datos reales etiquetados.

11. Trabajo futuro

- Obtener un conjunto de datos sísmicos reales con etiquetas verificadas.
- Entrenar y evaluar el modelo con señales reales.
- Evitar que registros relacionados o fragmentos de una misma señal aparezcan simultáneamente en entrenamiento y prueba.
- Comparar los resultados con métodos de referencia.
- Aplicar Integrated Gradients a señales reales de prueba.
- Analizar falsos positivos y falsos negativos.
- Documentar las condiciones en las que el sistema puede utilizarse y sus limitaciones.

12. Referencias

- Sundararajan, M., Taly, A. y Yan, Q. (2017). Axiomatic Attribution for Deep Networks. Proceedings of the 34th International Conference on Machine Learning.
- PyTorch. Documentación oficial: https://pytorch.org/docs/
- Captum. Documentación oficial: https://captum.ai/docs/
- ObsPy. Documentación oficial: https://docs.obspy.org/
- USGS. Earthquake Catalog: https://earthquake.usgs.gov/earthquakes/search/