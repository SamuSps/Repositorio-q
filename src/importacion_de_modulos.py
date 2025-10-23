import pandas as pd
import sqlite3
import os
import tkinter as tk
from tkinter import filedialog

def importar_datos(ruta_archivo):
    """
    Importa datos desde un archivo CSV, Excel o base de datos SQLite.
    Muestra las primeras filas para confirmar la carga.
    """
    if not os.path.exists(ruta_archivo):
        print("Error: El archivo no existe.")
        return None

    extension = os.path.splitext(ruta_archivo)[1].lower()

    try:
        if extension == '.csv':
            print("Cargando datos desde archivo CSV...")
            df = pd.read_csv(ruta_archivo)

        elif extension in ['.xlsx', '.xls']:
            print("Cargando datos desde archivo Excel...")
            df = pd.read_excel(ruta_archivo)

        elif extension in ['.sqlite', '.db']:
            print("Cargando datos desde base de datos SQLite...")
            conn = sqlite3.connect(ruta_archivo)
            tablas = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
            if tablas.empty:
                print("Error: No se encontró ninguna tabla en la base de datos.")
                return None

            nombre_tabla = tablas['name'][0]
            df = pd.read_sql_query(f"SELECT * FROM {nombre_tabla}", conn)
            conn.close()

        else:
            print("Error: Formato de archivo inválido.")
            return None

        # Mostrar vista previa
        print("\nDatos cargados correctamente. Vista previa:")
        print(df.head())

        # Mostrar tipos de datos detectados
        print("\nTipos de datos detectados:")
        print(df.dtypes)

        return df

    except ValueError as e:
        print(f"Error de formato o conversión: {e}")
    except sqlite3.DatabaseError as e:
        print(f"Error en la base de datos SQLite: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

    return None

def seleccionar_archivo():
    """
    Abre un diálogo para seleccionar archivos CSV, Excel o SQLite.
    """
    root = tk.Tk()
    root.withdraw()
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo de datos",
        filetypes=[
            ("CSV", "*.csv"),
            ("Excel", "*.xlsx *.xls"),
            ("SQLite", "*.sqlite *.db"),
            ("Todos", "*.*")
        ]
    )
    root.destroy()
    return archivo if archivo else None

def detectar_nans(df):
    """
    Detecta valores NaN por columna y devuelve un resumen.
    """
    nans_por_columna = df.isna().sum()
    total_nans = nans_por_columna.sum()
    resumen = f"Valores inexistentes (NaN) encontrados: {total_nans}\n"
    for col, count in nans_por_columna.items():
        if count > 0:
            resumen += f"- {col}: {count} NaN\n"
    return resumen if total_nans > 0 else "No se encontraron valores inexistentes."

def preprocesar_datos(df, metodo, columnas=None, valor_constante=None):
    """
    Preprocesa datos: elimina filas con NaN o rellena con media, mediana o constante.
    """
    if columnas:
        df = df[columnas].copy()  # Trabaja solo con columnas seleccionadas
    else:
        df = df.copy()
    
    try:
        if metodo == "eliminar":
            df = df.dropna()
        elif metodo == "media":
            df = df.fillna(df.mean(numeric_only=True))
        elif metodo == "mediana":
            df = df.fillna(df.median(numeric_only=True))
        elif metodo == "constante" and valor_constante is not None:
            df = df.fillna(valor_constante)
        else:
            raise ValueError("Método o valor constante inválido.")
        
        return df
    except Exception as e:
        raise ValueError(f"Error en preprocesamiento: {str(e)}")

# === Ejemplo de uso ===
if __name__ == "__main__":
    rutas = [
        "C:/Users/Elena/Documents/UDC/2IA/Software/Repositorio-q/docs/housing.csv",
        "C:/Users/Elena/Documents/UDC/2IA/Software/Repositorio-q/docs/housing.xlsx",
        "C:/Users/Elena/Documents/UDC/2IA/Software/Repositorio-q/docs/housing.db"
    ]

    for ruta in rutas:
        print("\n" + "="*80)
        df = importar_datos(ruta)
        if df is not None:
            print(detectar_nans(df))
            # Ejemplo de preprocesamiento
            df_procesado = preprocesar_datos(df, "media")
            print("\nDatos procesados (media):")
            print(df_procesado.head())