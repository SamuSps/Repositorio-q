import pytest
import os
import tempfile
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import joblib

# Supongamos que estas son tus funciones reales en modelo.py
from src.modelo import entrenar_modelo, predecir, guardar_modelo, cargar_modelo

@pytest.fixture
def df_sintetico():
    """Datos de prueba para entrenamiento y validación."""
    X = pd.DataFrame({
        "feature1": [1, 2, 3, 4, 5],
        "feature2": [2, 3, 4, 5, 6]
    })
    y = pd.Series([2, 4, 6, 8, 10])
    return X, y

def test_model_manage(df_sintetico):
    X, y = df_sintetico

    # --- 1. Entrenar modelo ---
    modelo = entrenar_modelo(X, y)
    assert isinstance(modelo, LinearRegression)

    # --- 2. Crear directorio temporal ---
    with tempfile.TemporaryDirectory() as tmpdir:
        ruta_modelo = os.path.join(tmpdir, "modelo_test.pkl")
        
        # --- 3. Guardar el modelo ---
        guardar_modelo(modelo, ruta_modelo)
        assert os.path.exists(ruta_modelo)

        # --- 4. Cargar el modelo ---
        modelo_cargado = cargar_modelo(ruta_modelo)
        assert isinstance(modelo_cargado, LinearRegression)

        # --- 5. Probar predicciones con modelo cargado ---
        y_pred = predecir(modelo_cargado, X)
        assert len(y_pred) == len(y)
        # Predicciones exactas para este dataset sintético
        np.testing.assert_array_almost_equal(y_pred, y.values)

        # --- 6. Validar campos del modelo ---
        # Verificar que coeficientes y intercept existen
        assert hasattr(modelo_cargado, "coef_")
        assert hasattr(modelo_cargado, "intercept_")
        assert len(modelo_cargado.coef_) == X.shape[1]

        # --- 7. Calcular métricas ---
        r2 = r2_score(y, y_pred)
        mse = mean_squared_error(y, y_pred)
        assert r2 >= 0.99  # cerca de 1 para datos sintéticos
        assert mse < 1e-6

        # --- 8. Guardar modelo en JSON (información mínima) ---
        ruta_json = os.path.join(tmpdir, "modelo_info.json")
        modelo_info = {
            "coef": modelo_cargado.coef_.tolist(),
            "intercept": modelo_cargado.intercept_.tolist() if isinstance(modelo_cargado.intercept_, np.ndarray) else modelo_cargado.intercept_
        }
        with open(ruta_json, "w") as f:
            json.dump(modelo_info, f)
        assert os.path.exists(ruta_json)

        # --- 9. Cargar modelo desde JSON ---
        with open(ruta_json, "r") as f:
            info_cargada = json.load(f)
        assert "coef" in info_cargada
        assert "intercept" in info_cargada
        assert info_cargada["coef"] == modelo_info["coef"]
