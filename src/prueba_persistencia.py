import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
import joblib
import os
import sys

# --- 1. Crear y Entrenar un Modelo Simple ---

# Datos de ejemplo
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# Crear y entrenar el modelo
model = LinearRegression()
model.fit(X, y)

# Hacer una predicción con el modelo original
try:
    pred_original = model.predict([[6]])
    print(f"Predicción Original (para X=6): {pred_original[0]}")
except Exception as e:
    print(f"Error al predecir con modelo original: {e}")
    sys.exit(1)


# --- 2. Guardar y Cargar con Joblib (RECOMENDADO) ---
print("\n--- Probando Joblib ---")
filename_joblib = 'modelo.joblib'

try:
    # Guardar el modelo
    joblib.dump(model, filename_joblib)
    print(f"Modelo guardado en {filename_joblib}")

    # Cargar el modelo
    loaded_model_joblib = joblib.load(filename_joblib)
    print("Modelo cargado desde Joblib.")

    # Verificar la predicción
    pred_joblib = loaded_model_joblib.predict([[6]])
    print(f"Predicción (Joblib): {pred_joblib[0]}")

except Exception as e:
    print(f"Error durante el proceso de Joblib: {e}")
    pred_joblib = [None] # Asignar un valor para que la aserción falle controladamente



# --- 3. Verificación Final ---
try:
    assert pred_original[0] == pred_joblib[0]
    print("\nLa prediccion coincide con la original.")
except AssertionError:
    print("\nLa prediccion no coincide.")
    print(f"  Original: {pred_original[0]}")
    print(f"  Joblib: {pred_joblib[0]}")

# --- 4. Limpieza de archivos ---
print("\nLimpiando archivos de prueba...")
try:
    if os.path.exists(filename_joblib):
        os.remove(filename_joblib)
        print(f"{filename_joblib} eliminado.")
except Exception as e:
    print(f"Error al limpiar archivos: {e}")