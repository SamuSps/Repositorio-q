import pytest
import pandas as pd
from src.importacion_de_modulos import preprocesar_datos, detectar_valores_faltantes

@pytest.fixture
def df_faltantes():
    """DataFrame de prueba con valores faltantes."""
    return pd.DataFrame({
        "A": [1, 2, None, 4],
        "B": [None, 2, 3, 4],
        "C": [1, 2, 3, 4]
    })

# --- Test: eliminar filas con valor faltante ---
def test_eliminar_filas(df_faltantes):
    df_proc = preprocesar_datos(df_faltantes, metodo="eliminar", columnas=["A", "B"])
    assert df_proc.isna().sum().sum() == 0
    # Solo quedan filas sin NaN
    assert len(df_proc) == 2

# --- Test: rellenar con media ---
def test_rellenar_media(df_faltantes):
    df_proc = preprocesar_datos(df_faltantes, metodo="media", columnas=["A", "B"])
    assert df_proc.isna().sum().sum() == 0
    # La media debe coincidir con el valor original reemplazado
    media_A = df_faltantes["A"].mean(skipna=True)
    media_B = df_faltantes["B"].mean(skipna=True)
    assert df_proc.loc[2, "A"] == media_A
    assert df_proc.loc[0, "B"] == media_B

# --- Test: rellenar con mediana ---
def test_rellenar_mediana(df_faltantes):
    df_proc = preprocesar_datos(df_faltantes, metodo="mediana", columnas=["A", "B"])
    assert df_proc.isna().sum().sum() == 0
    mediana_A = df_faltantes["A"].median(skipna=True)
    mediana_B = df_faltantes["B"].median(skipna=True)
    assert df_proc.loc[2, "A"] == mediana_A
    assert df_proc.loc[0, "B"] == mediana_B

# --- Test: rellenar con constante ---
def test_rellenar_constante(df_faltantes):
    df_proc = preprocesar_datos(df_faltantes, metodo="constante", columnas=["A", "B"], valor_constante=99)
    assert df_proc.isna().sum().sum() == 0
    assert df_proc.loc[2, "A"] == 99
    assert df_proc.loc[0, "B"] == 99

# --- Test: dataframe sin valores faltantes ---
def test_dataframe_sin_faltantes():
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    resumen = detectar_valores_faltantes(df)
    assert resumen == "No hay valores faltantes."

# --- Test: columna totalmente nula ---
def test_columna_nula():
    df = pd.DataFrame({"A": [None, None], "B": [1, 2]})
    df_proc = preprocesar_datos(df, metodo="constante", columnas=["A"], valor_constante=0)
    assert df_proc["A"].isna().sum() == 0


# --- Test: detección de valores faltantes ---
def test_deteccion_valores_faltantes(df_faltantes):
    resumen = detectar_valores_faltantes(df_faltantes)
    assert "A" in resumen and "B" in resumen
    assert "C" not in resumen  # no hay NaN en C

# --- Test: columna sin valor faltante se procesa correctamente ---
def test_columna_sin_faltante():
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df_proc = preprocesar_datos(df, metodo="media", columnas=["A", "B"])
    # Los valores deben mantenerse iguales
    pd.testing.assert_frame_equal(df, df_proc)
