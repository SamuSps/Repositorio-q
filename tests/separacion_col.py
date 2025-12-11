import pytest
import pandas as pd
from sklearn.model_selection import train_test_split
from importacion_de_modulos import preprocesar_datos

# --- Fixture: dataset de prueba ---
@pytest.fixture
def df_prueba():
    data = {
        "A": [1, 2, 3, 4, 5],
        "B": [5, 4, 3, 2, 1],
        "C": [10, 20, 30, 40, 50]
    }
    return pd.DataFrame(data)

# --- Test: separación 20/80 y 30/70, sin solapamiento, columnas numéricas ---
@pytest.mark.parametrize("test_size", [0.2, 0.3])
def test_columna_separacion(df_prueba, test_size):
    features = ["A", "B"]
    target = "C"

    # Preprocesamiento básico (no elimina nada)
    df_proc = preprocesar_datos(df_prueba, metodo="eliminar", columnas=features + [target])

    X = df_proc[features]
    y = df_proc[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    # --- Verificar proporciones ---
    total = len(df_proc)
    expected_test_len = int(total * test_size)
    expected_train_len = total - expected_test_len
    assert len(X_train) == expected_train_len
    assert len(X_test) == expected_test_len

    # --- Verificar que no hay solapamiento ---
    train_idx = set(X_train.index)
    test_idx = set(X_test.index)
    assert train_idx.isdisjoint(test_idx)

    # --- Verificar columnas numéricas ---
    assert all(pd.api.types.is_numeric_dtype(X_train[col]) for col in features)
    assert pd.api.types.is_numeric_dtype(y_train)

# --- Test: dataset muy pequeño ---
def test_dataset_pequeno():
    df_peq = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
    features = ["A", "B"]
    target = "C"
    df_proc = preprocesar_datos(df_peq, metodo="eliminar", columnas=features + [target])

    # División pequeña
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            df_proc[features], df_proc[target], test_size=0.5, random_state=42
        )
        assert len(X_train) > 0 and len(X_test) > 0
    except ValueError:
        pass  # aceptable para datasets muy pequeños

# --- Test: manejo de columnas inexistentes ---
def test_columnas_inexistentes(df_prueba):
    with pytest.raises(ValueError):
        preprocesar_datos(df_prueba, metodo="eliminar", columnas=["X", "Y"])

# --- Test: preprocesamiento con valor constante ---
def test_preprocesamiento_constante(df_prueba):
    df_nan = df_prueba.copy()
    df_nan.loc[0, "A"] = None
    df_proc = preprocesar_datos(df_nan, metodo="constante", columnas=["A"], valor_constante=99)
    assert df_proc.loc[0, "A"] == 99

# --- Test: preprocesamiento con media y mediana ---
def test_preprocesamiento_media_mediana(df_prueba):
    df_nan = df_prueba.copy()
    df_nan.loc[0, "A"] = None
    df_nan.loc[1, "B"] = None

    df_media = preprocesar_datos(df_nan, metodo="media", columnas=["A", "B"])
    df_mediana = preprocesar_datos(df_nan, metodo="mediana", columnas=["A", "B"])

    # Verificar que no quedan NaNs
    assert df_media[["A", "B"]].isna().sum().sum() == 0
    assert df_mediana[["A", "B"]].isna().sum().sum() == 0
