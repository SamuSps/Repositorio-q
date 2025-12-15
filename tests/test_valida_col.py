import pytest
import pandas as pd
import unittest

# Función auxiliar para validar que una columna sea numérica
def es_columna_numerica(columna: pd.Series) -> bool:
    """Devuelve True si la columna es numérica o se puede convertir a numérica, ignorando NaNs."""
    try:
        pd.to_numeric(columna.dropna())
        return True
    except:
        return False

# --- Fixture: DataFrames de prueba ---
@pytest.fixture
def df_numerica():
    return pd.DataFrame({"A": [1, 2, 3, 4]})

@pytest.fixture
def df_numerica_nan():
    return pd.DataFrame({"A": [1, 2, None, 4]})

@pytest.fixture
def df_texto():
    return pd.DataFrame({"A": ["a", "b", "c", "d"]})

@pytest.fixture
def df_mixto():
    return pd.DataFrame({"A": [1, 2, "b", 4]})

@pytest.fixture
def df_float():
    return pd.DataFrame({"A": [1.1, 2.2, 3.3, 4.4]})

@pytest.fixture
def df_string_num():
    return pd.DataFrame({"A": ["1", "2", "3", "4"]})

# --- Test: columna numérica ---
def test_columna_numerica(df_numerica):
    assert es_columna_numerica(df_numerica["A"]) == True

# --- Test: columna numérica con NaN ---
def test_columna_numerica_nan(df_numerica_nan):
    assert es_columna_numerica(df_numerica_nan["A"]) == True

# --- Test: columna texto ---
def test_columna_texto_falla(df_texto):
    assert es_columna_numerica(df_texto["A"]) == False

# --- Test: columna mixta num + texto ---
def test_columna_mixta_falla(df_mixto):
    assert es_columna_numerica(df_mixto["A"]) == False

# --- Test: columna float ---
def test_columna_float(df_float):
    assert es_columna_numerica(df_float["A"]) == True

# --- Test: columna string que representa número ---
def test_columna_string_num(df_string_num):
    assert es_columna_numerica(df_string_num["A"]) == True
if __name__ == "__main__":
    unittest.main()