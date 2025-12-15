Investigación: Persistencia de Modelos en Python

Historia de Usuario: Como desarrollador, quiero investigar cómo persistir datos a archivos en Python para poder guardar los modelos lineales creados y recuperarlos posteriormente.



1. Métodos de Persistencia Investigados

Se investigaron los dos métodos más comunes en el ecosistema de ciencia de datos de Python para guardar objetos: `pickle` y `joblib`.

    a. `pickle`
    Es la biblioteca estándar de Python para la serialización y deserialización de objetos "Serializar" (o "pickling") es el proceso de convertir un objeto de Python (como un diccionario, una lista, o incluso un modelo entrenado) en un flujo de bytes que puede ser escrito en un archivo.
    Biblioteca: `pickle` (incluida en Python por defecto).
    Uso: `pickle.dump(objeto, archivo)` y `pickle.load(archivo)`.
    
    b. `joblib`
    Es una biblioteca que forma parte del ecosistema de SciPy (y es mantenida por el equipo de Scikit-learn). Está diseñada para ser más eficiente en el manejo de objetos de Python que contienen grandes volúmenes de datos, especialmente arrays de NumPy.
    Biblioteca: `joblib` (se instala con `pip install joblib` o, más comúnmente, ya viene incluida como dependencia de `scikit-learn`).
    Uso: `joblib.dump(objeto, nombre_archivo)` y `joblib.load(nombre_archivo)`.



2. Documentación de Ventajas y Desventajas
La elección entre `pickle` y `joblib` depende casi exclusivamente del tipo de objeto que se desea guardar.

| Característica | `pickle` | `joblib` |
| :--- | :--- | :--- |
| Biblioteca | Estándar de Python (no requiere instalación). | Externa (dependencia de `scikit-learn` o `pip install joblib`). |
| Eficiencia (NumPy) | Baja. Es ineficiente para guardar objetos que contienen grandes arrays de NumPy (como los modelos de `sklearn`). Genera archivos más grandes y es más lento. | Alta. Está optimizado para NumPy. Guarda los arrays en archivos `.npy` separados, lo cual es mucho más rápido y resulta en archivos más pequeños. |
| Seguridad | Baja. Es un riesgo de seguridad conocido. Cargar un archivo `pickle` de una fuente no confiable puede ejecutar código malicioso. | Alta. Es más seguro que `pickle` y no es vulnerable a los mismos ataques de ejecución de código. |
| Facilidad de Uso | Alta. Muy sencillo de usar. | Alta. La API es casi idéntica a la de `pickle`. |
| Compatibilidad | Puede tener problemas entre diferentes versiones de Python. | Generalmente robusto, pero se recomienda usar la misma versión de `sklearn` y `joblib` al guardar y cargar. |

Veredicto para Modelos de Regresión Lineal

Para modelos de `scikit-learn` (como `LinearRegression`), `joblib` es el método preferido y recomendado oficialmente por el equipo de Scikit-learn.**

La razón principal es la eficiencia: un modelo de regresión lineal, aunque simple, almacena sus coeficientes (`coef_`) e intercepto (`intercept_`) como arrays de NumPy. `joblib` está optimizado para esto.



4. Documentación del Proceso (Pasos para el Equipo)
Paso 1: Importar
Teniendo `joblib` instalado se importa.

```python
import joblib
```

Paso 2: Guardar el Modelo
Después de entrenar el modelo, se usa `joblib.dump`.

```python
Suponiendo que 'self.modelo' es el objeto del modelo entrenado y 'ruta_guardado' es un string con la ruta (ej. "mi_modelo.joblib")
try:
     joblib.dump(self.modelo, ruta_guardado)
     print(f"Modelo guardado exitosamente en {ruta_guardado}")
 except Exception as e:
     print(f"Error al guardar el modelo: {e}")
 ```

Paso 3: Cargar el Modelo

Para recuperar el modelo, se usa `joblib.load`.

```python
 'ruta_archivo' es el path al archivo .joblib
 try:
     modelo_cargado = joblib.load(ruta_archivo)
     print(f"Modelo cargado desde {ruta_archivo}")
     Ahora se puede usar modelo_cargado.predict()
 except Exception as e:
     print(f"Error al cargar el modelo: {e}")