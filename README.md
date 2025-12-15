# PROYECTO Y DESCRIPCIÓN
Una aplicación intuitiva desarrollada en Python con la librería Tkinter que guía al usuario en la creacíon, evaluación, guardado y uso de modelos de regresión lineal utilizando scikit-learn. Ideal para cualquier persona que quiera aplicar regresión lineal sin escribir código.

# Propósito
Desarrollar una app que permita crear y visualizar modelos de regresión lineal simple [y múltiple] a partir de datos almacenados en archivos csv, excel, y bases de datos (SQLite), y hacer predicciones con ellos.

# Estructura
- `src/`: Código fuente.
- `files/`: Archivos para la ejecución.
- `docs/`: Documentación.
- `tests/`: Tests de pruebas.

# Características principales
- **Carga de datos**: Soporte para archivos CSV y Excel.
- **Previsualización** de los datos en una tabla.
- **Selección sencilla** de variables predictoras y variables objetivo.
- **Preprocesamiento** de valores faltantes (eliminar filas, rellenar con media o valor constante).
- **División automática** en conjuntos de entrenamiento y prueba (con control de porcentaje y semilla).
- **Entrenamiento** de modelo de Regresión Lineal.
- **Evaluación** con métricas (R² y Error Cuadrático Medio) en entrenamiento y prueba.
- **Visualización**:
  - Gráfico de ajuste.
  - Gráfico Real vs Predicho.
- **Fórmula legible** del modelo entrenado.
- **Descripción opcional** del modelo.
- **Guardado y carga** de modelos completos (incluye fórmula, métricas y descripción).
- **Predicción interactiva** con el modelo entrenado o cargado.

# Requisitos

- Python 3.8 o superior
- Librerías:
  - `pandas`
  - `numpy`
  - `scikit-learn`
  - `matplotlib`
  - `joblib`
  - `openpyxl` (para soporte Excel)

# Nota:
 La aplicación utiliza Tkinter, que viene incluido con la mayoría de instalaciones de Python. En algunas distribuciones de Linux, puede ser necesario instalarlo manualmente.

# Instrucciones de instalación y uso 

Instalación:
    Paso 1: Descarga el proyecto
    Puedes hacerlo bien clonando el repositorio con git o bien descargando el ZIP desde GitHub y descomprimirlo.
    Paso 2: Crea un entorno virtual (para evitar conflictos con otras instalaciones de python).
    Paso 3: Instala las dependencias (especificadas anteriormente).
Ejecución:
 Para ejecutar la aplicación simplemente en tu editor de python ejecuta el archivo main.py.
 
 Posteriormente se iniciará la aplicación y aparecerá una pantalla de bienvenida donde puedes cargar un modelo ya existente (Paso 0), en caso de hacer clic en siguiente accedes a la pantalla de carga de datos, donde debes seleccionar un archivo CSV o .xlsx (Paso 1).A continuación accedes a la pantalla de configuración y preprocesamiento, donde debes seleccionar una o múltiples variables predictoras y una sola objetivo, a su vez realizas la limpieza de valores faltantes ajustar el tamaño del conjunto de prueba y aplicar la configuración(Paso 2). El siguiente paso es la creación del modelo, que una vez creado verás la fórmula del modelo, las métricas, los gráficos, el panel de predicción, la descripción (opcional) y guardar modelo (Paso 4).

# Notas Técnicas para Desarrolladores y Colaboradores

Este documento está dirigido a desarrolladores que quieran entender, mantener, extender o contribuir al proyecto.

La aplicación es una GUI de escritorio monolítica escrita en Python utilizando:

- **Tkinter** como framework de interfaz gráfica.
- **Pandas** para manejo de datos.
- **scikit-learn** para el modelo de Regresión Lineal y métricas.
- **Matplotlib** integrado en Tkinter.
- **joblib** para serialización de modelos.

No se utilizan frameworks externos complejos, lo que facilita su mantenimiento y ejecución sin compilación.

Para más información sobre la contribución al proyecto leer documento "CONTRIBUTING.md"
