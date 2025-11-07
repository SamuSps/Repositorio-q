1. Introducción
El objetivo de esta historia es investigar y seleccionar librerías para la creación de modelos lineales en Python con el propósiton de aprender a construir, entrenar y evaluar un modelo predicitivo básico utilizando datos.
Además es necesario documentar el proceso seguido, las herramientas utilizadas y dificultades encontradas, para fortalecer la comprensión del equipo sobre los fundamentos de los modelos lineales.
________________________________________
2. Investigación de Librerías
Para el desarrollo de modelos lineales en Python, se investigaron las siguientes librerías populares y ampliamente utilizadas en la comunidad científica y de desarrollo:
Scikit-learn (sklearn):	Biblioteca enfocada en machine learning. Incluye algoritmos de regresión, clasificación, clustering y herramientas de preprocesamiento.Presenta las siguientes ventajas:
- Sintaxis sencilla y consistente.
- Amplia documentación y ejemplos.
- Facilita la división de datos y evaluación del modelo.
- Amplia comunidad de soporte.	
En relación a las desventajas:
- No ofrece análisis estadístico detallado (p-values, intervalos de confianza).
Statsmodels	:Biblioteca enfocada en la estadística clásica y econometría. Ideal para análisis e interpretación detallada de los coeficientes.	
Ventajas:
- Permite obtener métricas estadísticas completas.
- Ideal para análisis académicos.	
Desventajas:
- Requiere mayor conocimiento estadístico.
- Menos orientada al flujo de trabajo de machine learning.
Pandas:	Herramienta de manipulación y análisis de datos. Aunque no crea modelos, es esencial para preparar los datos antes del modelado.	
Ventajas:
- Permite limpiar, transformar y analizar datos fácilmente.
- Se integra con sklearn y statsmodels.
Desventajas:
- No implementa modelos de predicción.
Tras la comparación, se seleccionó Scikit-learn como la librería principal para la prueba de concepto, debido a su facilidad de uso, abundante documentación y orientación práctica hacia el machine learning.
________________________________________
3. Desarrollo del Modelo Lineal (Prueba de Concepto)
3.1 Objetivo
Construir y entrenar un modelo lineal simple utilizando la librería Scikit-learn, con el fin de comprender los pasos básicos del flujo de trabajo en machine learning: carga de datos, entrenamiento, evaluación y obtención de métricas.

3.2 Preparación del entorno
Se utilizaron las siguientes librerías de Python:
import pandas as pdimport numpy as npfrom sklearn.linear_model import LinearRegressionfrom sklearn.model_selection import train_test_splitfrom sklearn.metrics import mean_squared_error, r2_score

3.3 Carga y creación de datos
Para esta prueba se generaron datos sintéticos con una relación lineal entre una variable independiente X y una variable dependiente y.

np.random.seed(42)
X = np.random.rand(100, 1) * 10y = 3 * X.squeeze() + 5 + np.random.randn(100) * 2
data = pd.DataFrame({'X': X.squeeze(), 'y': y})

3.4 División de los datos
Se separaron los datos en conjuntos de entrenamiento (80%) y prueba (20%):

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

3.5 Entrenamiento del modelo
Se instanció y entrenó el modelo de regresión lineal utilizando la clase LinearRegression de scikit-learn.

model = LinearRegression()
model.fit(X_train, y_train)

3.6 Evaluación del modelo
Se realizaron predicciones sobre el conjunto de prueba y se calcularon métricas de evaluación:

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

Resultados obtenidos:
Métrica	               Valor
Coeficiente (pendiente)	2.95
Intersección         	5.20
 (MSE)	                3.90
 (R²)	                0.94

Estos resultados demuestran un buen ajuste del modelo, ya que el valor de R² (0.94) indica que el modelo explica aproximadamente el 94% de la variabilidad de los datos.
________________________________________
4. Dificultades encontradas y soluciones

Diferencias entre librerías: La elección entre statsmodels y scikit-learn generó dudas sobre cuál utilizar.	Se analizó la documentación oficial y se optó por scikit-learn por su sencillez.
Formato de los datos: scikit-learn requiere que X sea una matriz 2D y y un vector 1D. Se usó numpy.reshape() y train_test_split() para dar formato adecuado.
Interpretación de métricas:	Al principio no se comprendían bien las métricas MSE y R². Se revisó la teoría de regresión lineal y la documentación de sklearn.metrics.
________________________________________
5. Conclusiones
•Se investigaron y compararon distintas librerías para crear modelos lineales en Python, identificando sus ventajas y desventajas.
•Se seleccionó Scikit-learn por su facilidad de uso y documentación accesible.
•Se logró construir y entrenar un modelo lineal simple, evaluando su rendimiento mediante métricas estándar (MSE y R²).
•El equipo obtuvo una comprensión clara del flujo básico de trabajo en modelado lineal, desde la carga de datos hasta la evaluación del modelo.


