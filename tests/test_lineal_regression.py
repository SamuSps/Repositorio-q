import pytest
import numpy as np
import sys
import os

from sklearn.metrics import r2_score, mean_squared_error

# Permite importar desde src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from modelo import entrenar_modelo, predecir


# --------------------------------------------------
# Fixtures: datos sintéticos
# y = 2x + 1
# --------------------------------------------------
@pytest.fixture
def datos_entrenamiento():
    X = np.array([[1], [2], [3], [4], [5]])
    y = np.array([3, 5, 7, 9, 11])
    return X, y


@pytest.fixture
def datos_prueba():
    X_test = np.array([[6], [7]])
    y_test = np.array([13, 15])
    return X_test, y_test


# --------------------------------------------------
# Test: creación del modelo
# --------------------------------------------------
def test_creacion_modelo(datos_entrenamiento):
    X, y = datos_entrenamiento
    modelo = entrenar_modelo(X, y)

    assert modelo is not None
    assert hasattr(modelo, "predict")


# --------------------------------------------------
# Test: predicción correcta
# --------------------------------------------------
def test_prediccion_correcta(datos_entrenamiento, datos_prueba):
    X, y = datos_entrenamiento
    X_test, y_test = datos_prueba

    modelo = entrenar_modelo(X, y)
    pred = predecir(modelo, X_test)

    assert np.allclose(pred, y_test, atol=1e-6)


# --------------------------------------------------
# Test: coeficientes cercanos al valor esperado
# --------------------------------------------------
def test_coeficientes_modelo(datos_entrenamiento):
    X, y = datos_entrenamiento
    modelo = entrenar_modelo(X, y)

    coef = modelo.coef_[0]
    intercept = modelo.intercept_

    assert coef == pytest.approx(2.0, abs=1e-6)
    assert intercept == pytest.approx(1.0, abs=1e-6)


# --------------------------------------------------
# Test: generación de la fórmula del modelo
# y = ax + b
# --------------------------------------------------
def test_formula_modelo(datos_entrenamiento):
    X, y = datos_entrenamiento
    modelo = entrenar_modelo(X, y)

    a = modelo.coef_[0]
    b = modelo.intercept_

    formula = f"y = {a:.2f}x + {b:.2f}"

    assert formula.startswith("y =")
    assert "x" in formula
    assert "+" in formula or "-" in formula


# --------------------------------------------------
# Test: cálculo de R²
# --------------------------------------------------
def test_calculo_r2(datos_entrenamiento, datos_prueba):
    X, y = datos_entrenamiento
    X_test, y_test = datos_prueba

    modelo = entrenar_modelo(X, y)
    pred = predecir(modelo, X_test)

    r2 = r2_score(y_test, pred)
    assert r2 == pytest.approx(1.0, abs=1e-6)


# --------------------------------------------------
# Test: error cuadrático medio (MSE)
# --------------------------------------------------
def test_error_cuadratico_medio(datos_entrenamiento, datos_prueba):
    X, y = datos_entrenamiento
    X_test, y_test = datos_prueba

    modelo = entrenar_modelo(X, y)
    pred = predecir(modelo, X_test)

    mse = mean_squared_error(y_test, pred)
    assert mse == pytest.approx(0.0, abs=1e-6)


# --------------------------------------------------
# Test: modelo con variable constante
# y constante = 5
# --------------------------------------------------
def test_modelo_variable_constante():
    X = np.array([[1], [1], [1], [1]])
    y = np.array([5, 5, 5, 5])

    modelo = entrenar_modelo(X, y)
    pred = predecir(modelo, X)

    # Todas las predicciones deben ser constantes
    assert np.allclose(pred, y, atol=1e-6)

    # Coeficiente cercano a 0
    assert modelo.coef_[0] == pytest.approx(0.0, abs=1e-6)
