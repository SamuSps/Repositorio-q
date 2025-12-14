import pytest
import pandas as pd
import os
import sys
import sqlite3

# Permite importar desde src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from importacion_de_modulos import importar_datos


# --------------------------------------------------
# Fixture: DataFrame de prueba
# --------------------------------------------------
@pytest.fixture
def df_prueba():
    return pd.DataFrame({
        "A": [1, 2, 3],
        "B": [4, 5, None],
        "C": [7, 8, 9]
    })


# --------------------------------------------------
# Test: carga correcta de CSV
# --------------------------------------------------
def test_carga_csv(tmp_path, df_prueba):
    ruta = tmp_path / "datos.csv"
    df_prueba.to_csv(ruta, index=False)

    df = importar_datos(str(ruta))

    assert isinstance(df, pd.DataFrame)
    assert df.shape == df_prueba.shape


# --------------------------------------------------
# Test: carga correcta de Excel
# --------------------------------------------------
def test_carga_excel(tmp_path, df_prueba):
    ruta = tmp_path / "datos.xlsx"
    df_prueba.to_excel(ruta, index=False)

    df = importar_datos(str(ruta))

    assert isinstance(df, pd.DataFrame)
    assert df.shape == df_prueba.shape


# --------------------------------------------------
# Test: carga correcta de SQLite
# --------------------------------------------------
def test_carga_sqlite(tmp_path, df_prueba):
    ruta = tmp_path / "datos.sqlite"
    conn = sqlite3.connect(ruta)
    df_prueba.to_sql("tabla_test", conn, index=False)
    conn.close()

    df = importar_datos(str(ruta))

    assert isinstance(df, pd.DataFrame)
    assert df.shape == df_prueba.shape


# --------------------------------------------------
# Test: CSV con valores faltantes
# --------------------------------------------------
def test_csv_con_valores_faltantes(tmp_path):
    df_nan = pd.DataFrame({
        "A": [1, None, 3],
        "B": [4, 5, 6]
    })
    ruta = tmp_path / "datos_nan.csv"
    df_nan.to_csv(ruta, index=False)

    df = importar_datos(str(ruta))

    assert df.isna().sum().sum() > 0


# --------------------------------------------------
# Test: archivo inexistente
# --------------------------------------------------
def test_archivo_no_existente():
    with pytest.raises(FileNotFoundError):
        importar_datos("archivo_que_no_existe.csv")


# --------------------------------------------------
# Test: formato no soportado (.txt)
# --------------------------------------------------
def test_formato_no_soportado(tmp_path):
    ruta = tmp_path / "archivo.txt"
    ruta.write_text("contenido cualquiera")

    with pytest.raises(ValueError):
        importar_datos(str(ruta))


# --------------------------------------------------
# Test: CSV vacío
# --------------------------------------------------
def test_csv_vacio(tmp_path):
    ruta = tmp_path / "vacio.csv"
    ruta.write_text("")

    with pytest.raises(ValueError):
        importar_datos(str(ruta))
